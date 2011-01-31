import QtQuick 1.0

// The aim is to have text of a fixed width
// that fades per character not per whole string

// can this reuse the FadeText class?

Rectangle {
    id: page
    width: 200
    height: 200

    Row {
        Repeater {
            model: 3
            FadeText {
                text: "1"
                font.pointSize: 58
                font.bold: true
            }
        }
    }
/*    FadeText {
        id: char1
        text: "1"
        anchors.horizontalCenter: page.horizontalCenter
        anchors.verticalCenter: page.verticalCenter
    }
    FadeText {
        id: char2
        text: "2"
        anchors.left: char1.right
        anchors.bottom: char1.bottom
    }
    FadeText {
        text: "3"
        anchors.left: char2.right
        anchors.bottom: char2.bottom
    }*/

    // stuff to test
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
}

/*Text {
    id: container

    Behavior on text { 
        SequentialAnimation {
            NumberAnimation { target: container; properties: "opacity"; to: 0; duration: 400 }
            PropertyAction {}
            NumberAnimation { target: container; properties: "opacity"; to: 1; duration: 500 }
        }
    }
}*/
