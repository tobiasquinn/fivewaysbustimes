import Qt 4.7

Rectangle {
    Item {
        id: constants
        property int totalwidth: 600
        property int totalheight: 200
        property int rows: 5
        property int fixedrowheight: totalheight / rows
        property int animationduration: 250
    }
    width: 600
    height: 300
    ListModel {
        id: busesListModel

        ListElement {
            number: "5"
            arrivetime: "15:12"
            destination: "Somewhere"
        }
        ListElement {
            number: "N25"
            arrivetime: "05:43"
            destination: "Churchill Sq"
        }
        ListElement {
            number: "26"
            arrivetime: "19:30"
            destination: "Fiveways"
        }
    }

    // The delegate for each item in our model
    Component {
        id: listDelegate
        Rectangle {
            id: rec
            z: -index
            width: constants.totalwidth
            height:  constants.fixedrowheight
            color: ((index % 2 == 0) ? "#222" : "#111")
            Row {
                id: row
                anchors.bottom: parent.bottom
                FadeText {
                    //            id: arrivetime
                    text: arrivetime
                    color: "yellow"
                    font.bold: true
                    font.pixelSize: constants.fixedrowheight * 0.80
                    width: rec.width * 0.15
                    fadeduration: constants.animationduration
                }
                FadeText {
                    //            id: number
                    elide: Text.ElideRight
                    text: number
                    color: "white"
                    font.bold: true
                    font.pixelSize: constants.fixedrowheight * 0.80
                    width: rec.width * 0.10
                    fadeduration: constants.animationduration
                }
                FadeText {
                    //            id: destination
                    elide: Text.ElideRight
                    text: destination
                    color: "plum"
                    //font.italic: true
                    font.pixelSize: constants.fixedrowheight * 0.80
                    font.pointSize: 24
                    width: rec.width * 0.75
                    fadeduration: constants.animationduration
                }
            }
            ListView.onAdd: SequentialAnimation {
                PropertyAction { target: rec; property: "height"; value: 0 }
                NumberAnimation { target: rec; property: "height"; to: constants.fixedrowheight; duration: constants.animationduration; easing.type: Easing.InOutQuad }
            }

            ListView.onRemove: SequentialAnimation {
                PropertyAction { target: rec; property: "ListView.delayRemove"; value: true }
                PropertyAction { target: rec; property: "z"; value: -1000 } // not sure why this is needed
                NumberAnimation { target: rec; property: "height"; to: 0; duration: constants.animationduration; easing.type: Easing.InOutQuad }

                // Make sure delayRemove is set back to false so that the item can be destroyed
                PropertyAction { target: rec; property: "ListView.delayRemove"; value: false }
            }
        }
    }

    ListView {
        id: listView

        width: constants.totalwidth 
        height: constants.totalheight

        model: busesListModel
        delegate: listDelegate
    }

    Row {
        anchors { left: parent.left; bottom: parent.bottom; }
        TextButton {
            text: "Add a bus"
            onClicked: {
                busesListModel.append({
                    "number": "99",
                    "arrivetime": "98:76",
                    "destination": "Japan"
                })
            }
        }
        TextButton {
            text: "Remove last bus"
            onClicked: busesListModel.remove(busesListModel.count - 1)
        }
        TextButton {
            text: "Set item 2 val 1"
            onClicked: busesListModel.set(1, {"number": "54", "arrivetime": "12:43", "destination": "Germany"})
        }
       TextButton {
            text: "Set item 2 val 2"
            onClicked: busesListModel.set(1, {"number": "54", "arrivetime": "56:23", "destination": "Germany"})
        }
        TextButton {
            text: "insert"
            onClicked: {busesListModel.remove(1); busesListModel.insert(1, {"number": "12", "arrivetime" : "72:23", "destination": "Test"})}
        }
    }
}
