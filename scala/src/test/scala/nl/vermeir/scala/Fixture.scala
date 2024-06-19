package nl.vermeir.scala

import nl.vermeir.scala.controller.PESData
import nl.vermeir.scala.repository.{PESReader, PESRepository}
import org.joda.time.{DateTime, Days}
import scalikejdbc.{AutoSession, scalikejdbcSQLInterpolationImplicitDef}

object Fixture {
  implicit val session: AutoSession.type = AutoSession

  def recreate(): Unit = {
    sql"""
              drop table if exists CUSTOMER
         """.execute.apply()

    sql"""
              create table CUSTOMER (
              id varchar(64) not null primary key,
              name varchar(64),
              email varchar(64)
              )
         """.execute.apply()
  }

  def drop(): Boolean = {
    sql"""
             drop table if exists CUSTOMER
         """.execute.apply()
  }

  class MockPESReader extends PESReader {

    def constructBatchOfData(startOfInterval: DateTime, endOfInterval: DateTime, token: String): List[PESData] = {
      val daysCount = Days.daysBetween(startOfInterval, endOfInterval).getDays
      val theDate: DateTime = startOfInterval
      (0 until daysCount).map(d =>
        PESData(
          theDate.plusDays(d)
          , daysCount + d, 2*daysCount + d)
      ).toList
    }

    override def readDataFromWebsite(startOfInterval: DateTime, endOfInterval: DateTime, token: String): String = "\"00:00 tot 01:00 19 November 2016\";0,000;0,000;0,000;0,00;0,000"

    override def login(): String = "myToken"

    override def getData(csvData: (DateTime, DateTime, String) => String, startOfInterval: DateTime, endOfInterval: DateTime, token: String): List[PESData] = constructBatchOfData(startOfInterval, endOfInterval, token)
  }

  class MockPESRepository extends PESRepository {
    override def save(pesData: PESData): Unit = {}

    override def saveAll(pesData: List[PESData]): Unit = {}

    override def read(startOfInterval: DateTime, endOfInterval: DateTime): List[PESData] = {
      val daysCount = Days.daysBetween(startOfInterval, endOfInterval).getDays
      val theDate: DateTime = startOfInterval
      (0 until daysCount).map(d =>
        PESData(
          theDate.plusDays(d)
          , daysCount + d, 2*daysCount + d)
      ).toList
    }
  }

}