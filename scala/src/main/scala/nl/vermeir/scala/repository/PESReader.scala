package nl.vermeir.scala.repository

import com.github.nscala_time.time.Imports.DateTimeFormat
import nl.vermeir.scala.PESConfig.conf
import nl.vermeir.scala.controller.PESData
import org.joda.time.DateTime
import spray.json.DefaultJsonProtocol.{StringJsonFormat, jsonFormat1, jsonFormat2}
import spray.json._
import sttp.client4.quick._

import java.util.Locale

trait PESReader {
  def readDataFromWebsite(startOfInterval: DateTime, endOfInterval: DateTime, token: String): String

  def getData(csvData: (DateTime, DateTime, String) => String, startOfInterval: DateTime, endOfInterval: DateTime, token: String): List[PESData]

  def login(): String
}

class PESReaderImpl extends PESReader {

  private val dateOnlyFormat = DateTimeFormat.forPattern("yyyy-MM-dd")

  override def readDataFromWebsite(startOfInterval: DateTime, endOfInterval: DateTime, token: String): String = {
    val connectionId = conf.getString("connection_id")
    val startDate = dateOnlyFormat.print(startOfInterval)
    val endDate = dateOnlyFormat.print(endOfInterval)
    quickRequest
      .get(uri"https://dmp.pure-energie.nl/api/klantportaal/$connectionId/consumption/download?period=hours&start_date=$startDate&end_date=$endDate")
      .headers(Map(
        "User-Agent" -> "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv ->126.0) Gecko/20100101 Firefox/126.0",
        "Accept" -> "application/json",
        "Accept-Language" -> "en-US,en;q=0.5",
        "Accept-Encoding" -> "gzip, deflate, br, zstd",
        "Referer" -> "https ->//pure-energie.nl/",
        "X-Token" -> conf.getString("access_token"),
        "Origin" -> "https ->//pure-energie.nl",
        "Sec-Fetch-Dest" -> "empty",
        "Sec-Fetch-Mode" -> "cors",
        "Sec-Fetch-Site" -> "same-site",
        "DNT" -> "1",
        "Sec-GPC" -> "1",
        "authorization" -> f"Bearer ${token}",
        "TE" -> "trailers"
      ))
      .send()
      .body
  }

  private def getToken(data: String) = {
    final case class AccessToken(access_token: String)
    implicit val accessTokenFormat: RootJsonFormat[AccessToken] = jsonFormat1(AccessToken.apply)

    val token = data.parseJson.convertTo[AccessToken]
    token.access_token
  }

  private def getContent(response: String) = {
    final case class VerbruikContent(filename: String, content: String)
    implicit val verbruikContentFormat: RootJsonFormat[VerbruikContent] = jsonFormat2(VerbruikContent.apply)
    val jsonAst = response.parseJson
    jsonAst.convertTo[VerbruikContent].content
  }

  def login(): String = {
    val email = conf.getString("email")
    val password = conf.getString("password")
    val loginRequest = quickRequest
      .post(uri"https://dmp.pure-energie.nl/api/auth/login")
      .headers(Map(
        "User-Agent" -> "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv->126.0) Gecko/20100101 Firefox/126.0",
        "Accept" -> "application/json",
        "Accept-Language" -> "en-US,en;q=0.5",
        "Accept-Encoding" -> "gzip, deflate, br, zstd",
        "Content-Type" -> "application/json",
        "Referer" -> "https->//pure-energie.nl/",
        "Origin" -> "https->//pure-energie.nl",
        "Sec-Fetch-Dest" -> "empty",
        "Sec-Fetch-Mode" -> "cors",
        "Sec-Fetch-Site" -> "same-site",
        "DNT" -> "1",
        "Sec-GPC" -> "1",
        "Priority" -> "u=1",
        "TE" -> "trailers"))
      .body(
        s"""{"email": "${email}", "password": "${password}"}"""
      )
      .send()

    getToken(loginRequest.body)
  }

  override def getData(csvData: (DateTime, DateTime, String) => String, startOfInterval: DateTime, endOfInterval: DateTime, token: String): List[PESData] = {
    val data = getContent(csvData(startOfInterval, endOfInterval, token))
    data
      .split("\n")
      .filter(!skip(_))
      .map(parseLine)
      .toList
  }

  def parseLine(line: String): PESData = {
    // Periode;"Werkelijk verbruik";"Werkelijk verbruik (normaal)";"Werkelijk verbruik (dal)";"Werkelijk kosten";Teruglevering
    val parts: Array[String] = line.split(";")
    PESData(
      convertIntervalToDateTime(parts(0).replaceAll("\"", "")), parts(1).replace(',', '.').toFloat, parts(5).replace(',', '.').toFloat)
  }

  private def skip(s: String): Boolean =
    s.startsWith("Periode") || s.isEmpty

  private val dutchLocale = new Locale.Builder().setLanguage("nl").setRegion("NL").build()
  private val pesDateTimeFormatter = DateTimeFormat.forPattern("HH:mm dd MMMM yyyy").withLocale(dutchLocale)

  private def convertIntervalToDateTime(period: String): DateTime = {
    val timestamp = period.replaceAll(" tot .*? ", " ").toLowerCase()
    pesDateTimeFormatter.parseDateTime(timestamp)
  }

}

