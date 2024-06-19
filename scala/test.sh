#export JAVA_TOOL_OPTIONS="-XX:+TieredCompilation -XX:TieredStopAtLevel=1"
unset JAVA_TOOL_OPTIONS
java -jar target/scala-2.13/scalaVersion-assembly-1.0.jar &
P=`echo $!`
echo "$P"

#curl --silent --output /dev/null localhost:8080/customers
#curl localhost:8080/customers
curl --silent /dev/null localhost:8080/customers >/dev/null 2>&1
until [ $? -eq  0 ]
do
  curl --silent /dev/null curl localhost:8080/customers >/dev/null 2>&1
#  curl curl localhost:8080/customers
done

kill -9 "$P"