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

        onTextChanged: {
            console.log("Text changed")
        }
        // we want the text to fade out then in on a change
        onTimeChanged: {
            console.log("Time Changed" + time)
            timeText.text = time
            state = "textChange"
        }

        states: [
            State {
                name: "textChange";
//                when: text.changed
                PropertyChanges {
                    target: timeText
                }
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

    Text {
        id: goText
        text: "GO"
        anchors.horizontalCenter: page.horizontalCenter
        anchors.bottom: page.bottom

        MouseArea {
            id: mouseAreaGo
            anchors.fill: parent
            onClicked: {
                console.log("Clicked")
                var tn = new Date();
                timeText.time = tn.getHours() + ":" + tn.getMinutes() + ":" + tn.getSeconds()
            }
        }
    }

    Timer {
        interval: 1000
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
