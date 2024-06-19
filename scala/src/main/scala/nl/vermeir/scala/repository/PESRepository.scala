package nl.vermeir.scala.repository

import com.github.nscala_time.time.Imports.DateTime
import nl.vermeir.scala.controller.PESData
import scalikejdbc.TypeBinder.javaTimeLocalDateTimeDefault
import scalikejdbc._

import java.time.{LocalDateTime, ZoneId}
import scala.language.implicitConversions

trait PESRepository {
  def save(pesData: PESData): Unit
  def saveAll(pesData: List[PESData]): Unit
  def read(startTime: DateTime, endTime: DateTime): List[PESData]
}

class PESRepositoryImpl extends PESRepository {

  scalikejdbc.config.DBs.setupAll()

  implicit val session: AutoSession.type = AutoSession

  def save(pesData: PESData): Unit = {
    sql"""insert into verbruik_per_uur (period, total_usage, redelivery)
         values (${pesData.period}, ${pesData.total_usage}, ${pesData.redelivery})
         on duplicate key update
          total_usage = values(total_usage),
          redelivery = values(redelivery)
    """.update.apply()
  }

  def saveAll(pesData: List[PESData]): Unit = {
    // TODO: this is an inefficient implementation. how can i save a batch of data?
    pesData.foreach(save)
  }

  override def read(startTime: DateTime, endTime: DateTime): List[PESData] = {
    def convertLocalDateTimeToDateTime(localDateTime: LocalDateTime): DateTime =
     new DateTime(localDateTime.atZone(ZoneId.systemDefault())
       .toInstant
      .toEpochMilli)

    sql"""select * from verbruik_per_uur where period >= $startTime and period < $endTime""".map(rs => PESData(convertLocalDateTimeToDateTime(rs.get("period")), rs.get("total_usage"), rs.get("redelivery"))).list.apply()
  }
}