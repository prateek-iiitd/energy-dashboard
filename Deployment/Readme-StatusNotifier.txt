The RaspiStatusNotifier script is a way of monitoring all the Raspberry Pis that have been deployed in the campus from the server itself. It consists of a series of tests that are performed on each Raspberry Pi whose IP is listed in the "IP-List.txt" file. It is important to note that this is a server-side script and none of the tests are actually run on the Raspberry Pis. The tests are run on the server and the Raspberry Pis are inspected using the Local Network. In case there are some irregularities (test failures) for a sustained period of time, then they are reported by email.

The script consists of a series of 3 tests, each ensuring a certain level of functionality on the Raspberry Pi. The tests are conducted one after the other. Failing a test, on say Level 'x', would stop the testing procedure at this Level (x) and state in the report that is emailed where the failure occured (Level x in this case) along with a brief description of the test that it failed.

The tests listed in order are:

1. Ensuring network connectivity on the Raspberry Pi
This test pings the Raspberry Pi and checks if the device is responding to ICMP requests. An email notification is generated only if the Raspberry Pi fails to respond to ping requests for a period of more than 15 minutes. The test is conducted every 5 minutes and each test pings the Raspberry Pi 4 times. A failure is recorded only if all the ping requests in a test aren't responded to i.e. 100% packet loss. Failing the test 3 times consecutively would mean that the device hasn't responded for more than 15 minutes and would result in an event that will be reported.

2. Ensuring that the sMap service is running on port 8080.
This test observes whether the sMap instance is running on port 8080. It uses HTTP GET to inspect the device. The sMap service, when running, loads a standard HTML page that can be used to verify the sMap service is running. This test is conducted only if the preceeding test is passed. As in the previous case, 3 consecutive failures at tests conducted every 5 minutes would result in an email notification.

3. Ensuring new readings are being generated using sMap
This tests verifies that the sMap instance that is running hasn't stopped collecting data from the meters. This can occur due to some problems with 
modbus module, or some unhandled exception that may arise on the sMap source. This test requires failure on just 2 occasions (rather than 3) for a email notification to be generated.


Email Notification System
The email notification report that is generated is a combined report consisting of all tests that are currently marked as failed for the RasPis.
To ensure that this system doesn't spam the inbox with constant emails, once a test is marked failed and an email is sent for it, no further email notifications will be sent for the Raspberry Pi unless it first passes the test once. This way, it ensures that different emails correspond to two different instances of failures and there are as few redundancies as possible, at the same time reducing the number of emails being sent.

Once a Raspberry Pi qualifies for an event that is subject to notification (such as failing Tests1/2 on 3 occasions), then all other Raspberry Pis are inspected for tests that they are currently failing (even if they have failed just once or twice) and these tests are also part of the generated report. This way, it ensures that there is a single email in case of a mass failure. Otherwise, there would be separate emails for whenever the third failure occurs on different devices.
