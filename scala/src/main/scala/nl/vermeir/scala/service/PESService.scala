package nl.vermeir.scala.service

import com.github.nscala_time.time.Imports._
import nl.vermeir.scala.App.executionContext
import nl.vermeir.scala.controller.{PESData, UpdateResult}
import nl.vermeir.scala.repository.{PESReader, PESRepository}

import scala.concurrent.Future

class PESService(val pesReader: PESReader, val pesRepository: PESRepository) {
  private def findEndOfInterval(startDate: DateTime, endOfPeriod: DateTime): DateTime =
    minDate(startDate.plusDays(14), endOfPeriod)

  private def shouldIContinue(startOfInterval: DateTime, endDate: DateTime): Boolean =
    startOfInterval.compareTo(endDate) < 0

  private def minDate(date1: DateTime, date2: DateTime): DateTime =
    if (date1.compareTo(date2) < 0) date1 else date2

  def update(startDate: DateTime, endDate: DateTime): Future[UpdateResult] = {
    val token = pesReader.login()
    var count = 0
    var startOfInterval = startDate
    val endOfPeriod = minDate(endDate, DateTime.now().minusDays(1))
    while (shouldIContinue(startOfInterval, endOfPeriod)) {
      print(s"reading data from $startOfInterval")
      val endOfInterval = findEndOfInterval(startOfInterval, endOfPeriod)
      val newData = pesReader.getData(pesReader.readDataFromWebsite, startOfInterval, endOfInterval, token)
      println(s" found ${newData.length} records")
      pesRepository.saveAll(newData)
      startOfInterval = startOfInterval.plusDays(14)
      count = count + newData.length
    }

    val updateResult = UpdateResult("200", count)
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
