import Qt 4.7

Text {
    id: container
    property int fadeduration

    Behavior on text { 
        SequentialAnimation {
            NumberAnimation { target: container; properties: "opacity"; to: 0; duration: fadeduration / 2 }
            PropertyAction {}
            NumberAnimation { target: container; properties: "opacity"; to: 1; duration: fadeduration / 2 }
        }
    }
}
