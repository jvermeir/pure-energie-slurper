package nl.vermeir.scala.controller

import akka.http.scaladsl.model.{HttpEntity, HttpMethods, HttpRequest, MediaTypes}
import akka.http.scaladsl.testkit.ScalatestRouteTest
import akka.util.ByteString
import com.github.nscala_time.time.Imports.DateTime
import nl.vermeir.scala.{MockPESReader, MockPESRepository}
import nl.vermeir.scala.service.PESService
import org.scalatest.BeforeAndAfter
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec
import spray.json.DefaultJsonProtocol._
import spray.json._

class PESControllerTest extends AnyWordSpec with Matchers with ScalatestRouteTest with BeforeAndAfter {

  scalikejdbc.config.DBs.setupAll()

  implicit object DateTimeJsonFormat extends RootJsonFormat[DateTime] {
    def write(dateTime: DateTime): JsString = JsString(dateTime.toString)

    def read(value: JsValue): DateTime = value match {
      case JsString(dateTime: String) => DateTime.parse(dateTime)
      case _ => deserializationError("Expected dateTime format")
    }
  }
  implicit val updateResultFormat: RootJsonFormat[UpdateResult] = jsonFormat2(UpdateResult.apply)
  implicit val pesDataFormat: RootJsonFormat[PESData] = jsonFormat3(PESData.apply)

  private val updateRequestBody = ByteString(
    s"""{
       |"startDate":"2024-05-01"
       |, "endDate": "2024-06-01"
       |}
       |""".stripMargin
  )
  private val updateRequest = HttpRequest(
    HttpMethods.POST,
    uri = "/refresh",
    entity = HttpEntity(MediaTypes.`application/json`, updateRequestBody))

  private val readRequest = HttpRequest(
    HttpMethods.GET,
    uri = "/verbruik/2024-01-01/2024-01-03"
  )

  val mockReader = new MockPESReader()
  val mockPesRepository = new MockPESRepository()
  val mockService = new PESService(mockReader, mockPesRepository)
  val pesController = new PESController(mockReader, mockPesRepository)

  "PES controller" should {
    "update data when start and end date are given" in {
      updateRequest ~> pesController.route ~> check {
        status.isSuccess() shouldEqual true
        val result = parseUpdateResultFromResponse(responseAs[String])
        result.status shouldEqual "200"
        result.updatedRecords shouldEqual 31
      }
    }
    "return verbruik data" in {
      readRequest ~> pesController.route ~> check {
        status.isSuccess() shouldEqual true
        val result = parseReadResultFromResponse(responseAs[String])
        result.length shouldEqual 2
        result.map(_.redelivery).sum shouldEqual 9
        result.map(_.total_usage).sum shouldEqual 5
      }
    }
  }

  def parseReadResultFromResponse(readResponseAsString:String): List[PESData] =
    readResponseAsString.parseJson.convertTo[List[PESData]]

  def parseUpdateResultFromResponse(updateResultAsString: String): UpdateResult =
    updateResultAsString.parseJson.convertTo[UpdateResult]
}