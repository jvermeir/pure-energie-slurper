package nl.vermeir.scala.repository

import nl.vermeir.scala.controller.PESData
import org.joda.time.DateTime
import org.scalatest.BeforeAndAfter
import org.scalatest.funsuite.AnyFunSuite
import org.scalatest.matchers.should.Matchers

class PESRreaderImplTest extends AnyFunSuite with Matchers with BeforeAndAfter {
  test("parseLine constructs a PESData object from a valid line") {
    val result = new PESReaderImpl().parseLine("\"00:00 tot 01:00 19 November 2016\";1,000;2,000;3,000;4,00;5,000")

    result shouldEqual PESData( new DateTime(2016, 11, 19, 0, 0, 0), 1, 5)
  }
}
