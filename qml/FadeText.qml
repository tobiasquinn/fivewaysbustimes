import QtQuick 1.0

Text {
    id: container

    Behavior on text { 
        SequentialAnimation {
            NumberAnimation { target: container; properties: "opacity"; to: 0; duration: 400 }
            PropertyAction {}
            NumberAnimation { target: container; properties: "opacity"; to: 1; duration: 500 }
        }
    }
}
