package nl.vermeir.scala

import akka.actor.typed.ActorSystem
import akka.actor.typed.scaladsl.Behaviors
import akka.http.scaladsl.Http
import com.typesafe.config.Config
import nl.vermeir.scala.controller.PESController
import nl.vermeir.scala.repository.{PESReaderImpl, PESRepositoryImpl}

import scala.concurrent.ExecutionContext

object PESConfig {
  val conf: Config = com.typesafe.config.ConfigFactory.load("pesConfig.conf")
}

object App {
  implicit val system: ActorSystem[_] = ActorSystem(Behaviors.empty, "PESActorSystem")
  implicit val executionContext: ExecutionContext = system.executionContext

  val pesReader = new PESReaderImpl()
  val pesRepository = new PESRepositoryImpl()
  val pesController = new PESController(pesReader, pesRepository)

  def main(args: Array[String]): Unit = {

    Http().newServerAt("localhost", 8080).bind(pesController.route)

    println(s"\nHTTP REST interface: http://localhost:8080")
  }
}
