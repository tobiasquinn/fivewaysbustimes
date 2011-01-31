import QtQuick 1.0

Rectangle {
    id: page
    width: 500
    height: 200
    color: "lightgray"
    opacity: 1
    property alias text: timeText.text

    FadeText {
        id: timeText

        anchors.horizontalCenter: page.horizontalCenter
        anchors.verticalCenter: page.verticalCenter
        font.pointSize: 48
        font.bold: true
    }

    Timer {
        interval: 2000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: {
            console.log("Clock Timer Change")
            var tn = new Date();
            timeText.text = tn.getHours() + ":" + tn.getMinutes() + ":" + tn.getSeconds()
        }
    }
}
