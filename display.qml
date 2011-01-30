import QtQuick 1.0

Rectangle {
    id: page
    width: 500
    height: 200
    color: "lightgray"
    opacity: 1

    Text {
        id: timeText

        property string time: "1"

        anchors.horizontalCenter: page.horizontalCenter
        anchors.verticalCenter: page.verticalCenter
        font.pointSize: 48; font.bold: true
        state: "fadedin"

        MouseArea {
            id: mouseArea
            anchors.fill: parent
        }

        // we want the text to fade out then in on a change
        onTimeChanged: {
            console.log("Time Changed" + time)
            state = "fadedout"
        }

        states: [
            State {
                name: "fadedout"
                PropertyChanges {
                    target: timeText
                    opacity: 0
                }
            },
            State {
                name: "fadedin"
                PropertyChanges {
                    target: timeText
                    opacity: 1
                }
            }
        ]

        transitions: [
            Transition {
                from: "fadedin"; to: "fadedout"
                SequentialAnimation {
                    NumberAnimation {
                        properties: "opacity"
                        duration: 400
                        easing.type: Easing.OutQuad
                    }
                    PropertyAction { target: timeText; property: "state"; value: "fadedin" }
                }
            },
            Transition {
                from: "fadedout"; to: "fadedin"
                SequentialAnimation {
                    PropertyAction { target: timeText; property: "text"; value: timeText.time }
                    NumberAnimation {
                        properties: "opacity"
                        duration: 800
                        easing.type: Easing.InQuad
                    }
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
                timeText.time = parseInt(timeText.time) + 1
            }
        }
    }
}
