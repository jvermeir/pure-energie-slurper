package nl.vermeir.scala.controller

import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.server.Route
import com.github.nscala_time.time.Imports.{DateTime, DateTimeFormat}
import nl.vermeir.scala.PESConfig
import nl.vermeir.scala.repository.{PESReader, PESRepository}
import nl.vermeir.scala.service.PESService
import spray.json.DefaultJsonProtocol._
import spray.json.{JsString, JsValue, RootJsonFormat, deserializationError}

final case class UpdateRequest(startDate: Option[String] = None, endDate: Option[String] = None, method: String = "par")

final case class ReadDataResult(result: List[PESData])

final case class UpdateResult(status: String, updatedRecords: Int)

final case class PESData(period: DateTime, total_usage: Float, redelivery: Float)

class PESController(pesReader: PESReader, pesRepository: PESRepository) {

  implicit object DateTimeJsonFormat extends RootJsonFormat[DateTime] {
    def write(dateTime: DateTime): JsString = JsString(dateTime.toString)

    def read(value: JsValue): DateTime = value match {
      case JsString(dateTime: String) => DateTime.parse(dateTime)
      case _ => deserializationError("Expected dateTime format")
    }
  }

  implicit val updateRequestFormat: RootJsonFormat[UpdateRequest] = jsonFormat3(UpdateRequest.apply)
  implicit val updateResultFormat: RootJsonFormat[UpdateResult] = jsonFormat2(UpdateResult.apply)
  implicit val pesDataFormat: RootJsonFormat[PESData] = jsonFormat3(PESData.apply)
  implicit val readVerbruikFormat: RootJsonFormat[ReadDataResult] = jsonFormat1(ReadDataResult.apply)

  private def getStartDate(startDate: Option[String]): DateTime = {
    println(s"$startDate startdate")
    DateTime.parse(startDate.getOrElse(PESConfig.conf.getString("start_of_data")), DateTimeFormat.forPattern("yyyy-MM-dd"))
  }

  private def getEndDate(endDate: Option[String]): DateTime = {
    println(s"$endDate enddate")
    lazy val yesterday = DateTimeFormat.forPattern("yyyy-MM-dd").print(DateTime.yesterday())
    DateTime.parse(endDate.getOrElse(yesterday), DateTimeFormat.forPattern("yyyy-MM-dd"))
  }

  val route: Route =
    concat(
      update,
      query
    )

  private def query = {
    get {
      pathPrefix("verbruik" / Segment / Segment) { (startDateParam, endDateParam) =>
        val startDate = getStartDate(Some(startDateParam))
        val endDate = getEndDate(Some(endDateParam))

        val verbruikData = new PESService(pesReader, pesRepository).read(startDate, endDate)
        onSuccess(verbruikData) { _ => complete(verbruikData) }
      }
    }
  }

  private def update = {
    path("refresh") {
      post {
        entity(as[UpdateRequest]) { updateRequest =>
          val startDate = getStartDate(updateRequest.startDate)
          val endDate = getEndDate(updateRequest.endDate)

          val result = updateRequest.method match {
            case "par" => new PESService(pesReader, pesRepository).updatePar(startDate, endDate)
            case "stream" => new PESService(pesReader, pesRepository).update(startDate, endDate)
            case "actors" => new PESService(pesReader, pesRepository).updateActors(startDate, endDate)
            case _ => new PESService(pesReader, pesRepository).updateImperativeVersion(startDate, endDate)
          }
          onSuccess(result) { _ => complete(result) }
        }
      }
    }
  }
}