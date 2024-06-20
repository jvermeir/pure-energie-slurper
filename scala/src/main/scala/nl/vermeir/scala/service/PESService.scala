package nl.vermeir.scala.service

import akka.NotUsed
import akka.stream.FlowShape
import akka.stream.scaladsl._
import com.github.nscala_time.time.Imports._
import com.typesafe.scalalogging.Logger
import nl.vermeir.scala.App.{executionContext, system}
import nl.vermeir.scala.controller.{PESData, UpdateResult}
import nl.vermeir.scala.repository.{PESReader, PESRepository}
import org.joda.time.Days

import java.util.concurrent.TimeUnit
import scala.collection.parallel.CollectionConverters.ArrayIsParallelizable
import scala.concurrent.{Await, Future}

class PESService(val pesReader: PESReader, val pesRepository: PESRepository) {
  private val logger = Logger("Service")

  private def findEndOfInterval(startDate: DateTime, endOfPeriod: DateTime): DateTime =
    minDate(startDate.plusDays(14), endOfPeriod)

  private def shouldIContinue(startOfInterval: DateTime, endDate: DateTime): Boolean =
    startOfInterval.compareTo(endDate) < 0

  private def minDate(date1: DateTime, date2: DateTime): DateTime =
    if (date1.compareTo(date2) < 0) date1 else date2

  private def updateDataForInterval(startOfInterval: DateTime, endOfPeriod: DateTime, token: String): Int = {
    logger.info(s"reading data from $startOfInterval")
    val endOfInterval = findEndOfInterval(startOfInterval, endOfPeriod)
    val newData = pesReader.getData(pesReader.readDataFromWebsite, startOfInterval, endOfInterval, token)
    logger.info(s" found ${newData.length} records")
    pesRepository.saveAll(newData)
    newData.length
  }

  @Deprecated
  def updateImperativeVersion(startDate: DateTime, endDate: DateTime): Future[UpdateResult] = {
    logger.info("imperative update")
    val token = pesReader.login()
    var count = 0
    var startOfInterval = startDate
    val endOfPeriod = minDate(endDate, DateTime.now().minusDays(1))
    while (shouldIContinue(startOfInterval, endOfPeriod)) {
      val newRecordCount = updateDataForInterval(startOfInterval, endOfPeriod, token)
      count = count + newRecordCount
      startOfInterval = startOfInterval.plusDays(14)
    }

    logger.info(s"updated $count records")
    val updateResult = UpdateResult("200", count)
    Future {
      updateResult
    }
  }

  def update(startDate: DateTime, endDate: DateTime): Future[UpdateResult] = {
    logger.info("sequential update")
    val token = pesReader.login()
    val endOfPeriod = minDate(endDate, DateTime.now().minusDays(1))
    val days: Int = Days.daysBetween(startDate, endDate).getDays
    val numberOfDaysUpdated = (0 to days by 14).to(LazyList)
      .map(i => {
        updateDataForInterval(startDate.plusDays(i), endOfPeriod, token)
      })
      .sum

    logger.info(s"updated $numberOfDaysUpdated records")
    val updateResult = UpdateResult("200", numberOfDaysUpdated)
    Future {
      updateResult
    }
  }

  def updatePar(startDate: DateTime, endDate: DateTime): Future[UpdateResult] = {
    logger.info("par update")
    val token = pesReader.login()
    val endOfPeriod = minDate(endDate, DateTime.now().minusDays(1))
    val days: Int = Days.daysBetween(startDate, endDate).getDays

    val data = (0 to days by 14).toArray.par
// TODO: why is this ignored? data.tasksupport = new ForkJoinTaskSupport(new ForkJoinPool(2))
    val numberOfDaysUpdated =
      data
      .map(i => updateDataForInterval(startDate.plusDays(i), endOfPeriod, token))
      .sum

    logger.info(s"updated $numberOfDaysUpdated records")
    val updateResult = UpdateResult("200", numberOfDaysUpdated)
    Future {
      updateResult
    }
  }

  def updateActors(startDate: DateTime, endDate: DateTime): Future[UpdateResult] = {
    type Result = Int

    logger.info("par update")
    val token = pesReader.login()
    val endOfPeriod = minDate(endDate, DateTime.now().minusDays(1))
    val days: Int = Days.daysBetween(startDate, endDate).getDays
    val data = Source(0 to days by 14)

    val worker = Flow[Int].map(i => {
      updateDataForInterval(startDate.plusDays(i), endOfPeriod, token)
    })

    def balancer[In, Out](worker: Flow[In, Out, Any], workerCount: Int): Flow[In, Out, NotUsed] = {
      import GraphDSL.Implicits._

      Flow.fromGraph(GraphDSL.create() { implicit b =>
        val balancer = b.add(Balance[In](workerCount, waitForAllDownstreams = true))
        val merge = b.add(Merge[Out](workerCount))

        for (_ <- 1 to workerCount) {
          balancer ~> worker.async ~> merge
        }

        FlowShape(balancer.in, merge.out)
      })
    }

    val processedJobs: Source[Result, NotUsed] = data.via(balancer(worker, 3))
    val updateCounts = Await.result(processedJobs.limit(10).runWith(Sink.seq), scala.concurrent.duration.Duration(50, TimeUnit.SECONDS))
    val updateResult = UpdateResult("200", updateCounts.sum)

    Future {
      updateResult
    }
  }

  def read(startTime: DateTime, endTime: DateTime): Future[List[PESData]] = {
    Future {
      pesRepository.read(startTime, endTime)
    }
  }
}
