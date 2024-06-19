package nl.vermeir.scala.service

import nl.vermeir.scala.Fixture.{MockPESReader, MockPESRepository, drop, recreate}
import org.joda.time.DateTime
import org.scalatest.BeforeAndAfter
import org.scalatest.funsuite.AnyFunSuite
import org.scalatest.matchers.should.Matchers

import scala.concurrent.Await
import scala.concurrent.duration.Duration

class PESServiceTest extends AnyFunSuite with Matchers with BeforeAndAfter {
  scalikejdbc.config.DBs.setupAll()

  val mockReader = new MockPESReader()
  val mockPESRepository = new MockPESRepository()

  before(recreate())
  after(drop())

  test("read data for a 15 day period from service") {
    val service = new PESService(mockReader, mockPESRepository)
    val data = service.update(DateTime.now().minusDays(16), DateTime.now().minusDays(1))
    val result = Await.result(data, Duration(5, "seconds"))

    assert(result.status == "200")
    assert(result.updatedRecords == 15)
  }

  test("read data for a 14 day period from service") {
    val service = new PESService(mockReader, mockPESRepository)
    val data = service.update(DateTime.now().minusDays(15), DateTime.now().minusDays(1))
    val result = Await.result(data, Duration(5, "seconds"))
    result.status shouldEqual "200"
    result.updatedRecords shouldEqual 14
  }

  test("read data for a 1 day period from service") {
    val service = new PESService(mockReader, mockPESRepository)
    val data = service.update(DateTime.now().minusDays(2), DateTime.now().minusDays(1))
    val result = Await.result(data, Duration(5, "seconds"))

    result.status shouldEqual "200"
    result.updatedRecords shouldEqual 1
  }

  test("no data if we try to read only today") {
    val service = new PESService(mockReader, mockPESRepository)
    val data = service.update(DateTime.now().minusDays(1), DateTime.now())
    val result = Await.result(data, Duration(5, "seconds"))

    result.status shouldEqual "200"
    result.updatedRecords shouldEqual 0
  }

  test("no data in the future") {
    val service = new PESService(mockReader, mockPESRepository)
    val data = service.update(DateTime.now().plusDays(1), DateTime.now())
    val result = Await.result(data, Duration(5, "seconds"))

    result.status shouldEqual "200"
    result.updatedRecords shouldEqual 0
  }

  test("read retrieves verbruikdata between two dates") {
    val service = new PESService(mockReader, mockPESRepository)
    val data = service.read(DateTime.now.minusDays(3), DateTime.now().minusDays(1))
    val result = Await.result(data, Duration(5, "seconds"))

    result.length shouldEqual  2
    result.map(_.total_usage).sum shouldEqual 5
    result.map(_.redelivery).sum shouldEqual 9
  }
}
