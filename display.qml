import QtQuick 1.0

Rectangle {
    id: page
    width: 500
    height: 200
    color: "lightgray"
    opacity: 1

    Text {
        id: busnumberText
        text: "25"
        anchors.horizontalCenter: page.horizontalCenter
        anchors.verticalCenter: page.verticalCenter
        font.pointSize: 48; font.bold: true

        MouseArea {
            id: mouseArea
            anchors.fill: parent
        }

/*        Rectangle {
            anchors.fill: parent
            color: "tomato"
            opacity: 0.33
        }*/

        // we want the text to fade in the out on a change
        states: State {
            name: "fadeout"
            when: mouseAreaGo.pressed == true
            PropertyChanges {
                target: busnumberText
                opacity: 0
            }   
        }

        transitions: Transition {
            from: ""; to: "fadeout";
            ParallelAnimation {
                NumberAnimation {
                    properties: "opacity"
                    duration: 800
                    easing.type: Easing.OutQuad
                }
            }
        }
    }

    Text {
        id: goText
        text: "GO"
        anchors.horizontalCenter: page.horizontalCenter
        anchors.bottom: page.bottom

        MouseArea {
            id: mouseAreaGo
            anchors.fill: parent
        }
    }
}
