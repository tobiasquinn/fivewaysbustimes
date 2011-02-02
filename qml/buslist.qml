import Qt 4.7

ListView {
    id: pythonListView

    width: 400
    height: 200

    model: pythonListModel

    delegate: Component {
        id: col
        Rectangle {
            width: pythonListView.width
            height: 40
            color: ((index % 2 == 0) ? "#222" : "#111")
            Text {
                id: number
                elide: Text.ElideRight
                text: model.Bus.number
                color: "white"
                font.bold: true
                anchors.leftMargin: 10
                anchors.left: parent.left
            }
            Text {
                id: destination
                elide: Text.ElideRight
                text: model.Bus.destination
                color: "plum"
                font.italic: true
                anchors.leftMargin: 10
                anchors.left: number.right
            }
            FadeText {
                id: arrivetime
                text: model.Bus.arrivetime
                color: "yellow"
                font.bold: true
                anchors.leftMargin: 10
                anchors.left: destination.right
            }
        }
    }
}
