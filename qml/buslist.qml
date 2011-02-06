import Qt 4.7

Rectangle {
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
            width: listView.width
            height:  listView.rowheight
            color: ((index % 2 == 0) ? "#222" : "#111")
            Row {
                FadeText {
                    //            id: arrivetime
                    text: arrivetime
                    color: "yellow"
                    font.bold: true
                    font.pixelSize: rec.height * 0.80
                    width: rec.width * 0.15
                }
                Text {
                    //            id: number
                    elide: Text.ElideRight
                    text: number
                    color: "white"
                    font.bold: true
                    font.pixelSize: rec.height * 0.80
                    width: rec.width * 0.10
                }
                Text {
                    //            id: destination
                    elide: Text.ElideRight
                    text: destination
                    color: "plum"
                    font.italic: true
                    font.pixelSize: rec.height * 0.80
                    width: rec.width * 0.75
                }
            }
            ListView.onAdd: SequentialAnimation {
                PropertyAction { target: rec; property: "height"; value: 0 }
                NumberAnimation { target: rec; property: "height"; to: listView.rowheight; duration: 250; easing.type: Easing.InOutQuad }
            }

            ListView.onRemove: SequentialAnimation {
                PropertyAction { target: rec; property: "ListView.delayRemove"; value: true }
                NumberAnimation { target: rec; property: "height"; to: 0; duration: 250; easing.type: Easing.InOutQuad }

                // Make sure delayRemove is set back to false so that the item can be destroyed
                PropertyAction { target: rec; property: "ListView.delayRemove"; value: false }
            }
        }
    }

    ListView {
        id: listView

        width: 600
        height: 200
        property int rows: 5
        property int rowheight: height / rows

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
    }
}
