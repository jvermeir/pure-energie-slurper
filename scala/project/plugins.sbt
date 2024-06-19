addSbtPlugin("io.spray" % "sbt-revolver" % "0.10.0")

resolvers += "Akka library repository".at("https://repo.akka.io/maven")
addSbtPlugin("com.lightbend.akka.grpc" % "sbt-akka-grpc" % "2.4.3")

addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "0.15.0")
