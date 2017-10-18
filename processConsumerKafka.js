var getTimestamp = function()
{
    var today = new Date();
    var mm = today.getMonth()+1; 
    var day = today.getDate();
    var yyyy = today.getFullYear();
    var minute = today.getMinutes();
    var hour = today.getHours();
    var seconds = today.getSeconds();

    var mmString = mm.toLocaleString('en', {minimumIntegerDigits:2})
    var dayString = day.toLocaleString('en', {minimumIntegerDigits:2})
    var yearString = yyyy.toLocaleString('en', {minimumIntegerDigits:4})
    var hourString = hour.toLocaleString('en', {minimumIntegerDigits:2})
    var minutesString = minute.toLocaleString('en', {minimumIntegerDigits:2})
    var secondsString = seconds.toLocaleString('en', {minimumIntegerDigits:2})
    var output =  yearString+'-'+mmString+'-'+dayString+' '+hourString+':'+minutesString+':'+secondsString
    output.replace(',', '')
    return output
}

var flowFile = session.get();
if (flowFile != null) {
    var route = REL_FAILURE;
    var StreamCallback = Java.type("org.apache.nifi.processor.io.StreamCallback");
    var IOUtils = Java.type("org.apache.commons.io.IOUtils");
    var StandardCharsets = Java.type("java.nio.charset.StandardCharsets");
    flowFile = session.write(flowFile,
        new StreamCallback(function (inputStream, outputStream) {
            var text = IOUtils.toString(inputStream, StandardCharsets.UTF_8);
            var json = JSON.parse(text);
            var key = flowFile.getAttribute("kafka.key");
            var topic = flowFile.getAttribute("kafka.topic");

            if (key != null && topic != null) {
                var output = { };
                output['topic'] = topic;
                output['key'] = key
                output['value'] = json
                output['timestamp'] = getTimestamp()
                route = REL_SUCCESS;
            }
            outputStream.write(JSON.stringify(output).getBytes(StandardCharsets.UTF_8));
    }));
    session.transfer(flowFile, route)
}

