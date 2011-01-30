import QtQuick 1.0

Rectangle {
    id: page
    width: 500
    height: 200
    color: "lightgray"
    opacity: 1

    Text {
        id: timeText

        property string time

        anchors.horizontalCenter: page.horizontalCenter
        anchors.verticalCenter: page.verticalCenter
        font.pointSize: 48
        font.bold: true
        state: "normal"

        MouseArea {
            id: mouseArea
            anchors.fill: parent
        }

        onTimeChanged: {
            console.log("Time Changed: " + time)
            state = "textChange"
        }

        states: [
            State {
                name: "textChange";
            }
        ]

        transitions: [
            Transition {
                from: "normal"; to: "textChange"
                SequentialAnimation {
                    NumberAnimation { target: timeText; properties: "opacity"; to: 0; duration: 400 }
                    PropertyAction { target: timeText; property: "text"; value: timeText.time }
                    NumberAnimation { target: timeText; properties: "opacity"; to: 1; duration: 500 }
                    PropertyAction { target: timeText; property: "state"; value: "normal" }
                }
            }
        ]
    }

    Timer {
        interval: 2000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: {
            console.log("Clock Timer Change")
            var tn = new Date();
            timeText.time = tn.getHours() + ":" + tn.getMinutes() + ":" + tn.getSeconds()
        }
    }
}
