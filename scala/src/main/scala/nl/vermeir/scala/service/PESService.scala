package nl.vermeir.scala.service

import com.github.nscala_time.time.Imports._
import nl.vermeir.scala.App.executionContext
import nl.vermeir.scala.controller.{PESData, UpdateResult}
import nl.vermeir.scala.repository.{PESReader, PESRepository}
import org.joda.time.Days

import scala.concurrent.Future

class PESService(val pesReader: PESReader, val pesRepository: PESRepository) {
  private def findEndOfInterval(startDate: DateTime, endOfPeriod: DateTime): DateTime =
    minDate(startDate.plusDays(14), endOfPeriod)

  private def shouldIContinue(startOfInterval: DateTime, endDate: DateTime): Boolean =
    startOfInterval.compareTo(endDate) < 0

  private def minDate(date1: DateTime, date2: DateTime): DateTime =
    if (date1.compareTo(date2) < 0) date1 else date2

  private def updateDataForInterval(startOfInterval: DateTime, endOfPeriod: DateTime, token: String): Int = {
    print(s"reading data from $startOfInterval")
    val endOfInterval = findEndOfInterval(startOfInterval, endOfPeriod)
    val newData = pesReader.getData(pesReader.readDataFromWebsite, startOfInterval, endOfInterval, token)
    println(s" found ${newData.length} records")
    pesRepository.saveAll(newData)
    newData.length
  }

  @Deprecated
  def updateImperativeVersion(startDate: DateTime, endDate: DateTime): Future[UpdateResult] = {
    val token = pesReader.login()
    var count = 0
    var startOfInterval = startDate
    val endOfPeriod = minDate(endDate, DateTime.now().minusDays(1))
    while (shouldIContinue(startOfInterval, endOfPeriod)) {
      val newRecordCount = updateDataForInterval(startOfInterval, endOfPeriod, token)
      count = count + newRecordCount
      startOfInterval = startOfInterval.plusDays(14)
    }

    val updateResult = UpdateResult("200", count)
    Future {
      updateResult
    }
  }

  def update(startDate: DateTime, endDate: DateTime): Future[UpdateResult] = {
    val token = pesReader.login()
    val endOfPeriod = minDate(endDate, DateTime.now().minusDays(1))
    val days: Int = Days.daysBetween(startDate, endDate).getDays
    val numberOfDaysUpdated = (0 to days by 14).to(LazyList)
      .map(i => {
        updateDataForInterval(startDate.plusDays(i), endOfPeriod, token)
      })
      .sum

    val updateResult = UpdateResult("200", numberOfDaysUpdated)
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
