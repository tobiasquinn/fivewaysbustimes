import Qt 4.7

ListView {
    id: plv

    width: 600
    height: 200
    property int rows: 5
    property int rowheight: height / rows

    model: pythonListModel

    delegate: Component {
        id: col
        Rectangle {
            width: plv.width
            height:  plv.rowheight
            color: ((index % 2 == 0) ? "#222" : "#111")
            FadeText {
                id: arrivetime
                text: model.Bus.arrivetime
                color: "yellow"
                font.bold: true
                font.pixelSize: parent.height * 0.80
                width: parent.width * 0.15
//                anchors.leftMargin: 10
                anchors.left: parent.left
            }
            Text {
                id: number
                elide: Text.ElideRight
                text: model.Bus.number
                color: "white"
                font.bold: true
                font.pixelSize: parent.height * 0.80
                width: parent.width * 0.10
//                anchors.leftMargin: 10
                anchors.left: arrivetime.right
            }
            Text {
                id: destination
                elide: Text.ElideRight
                text: model.Bus.destination
                color: "plum"
                font.italic: true
                font.pixelSize: parent.height * 0.80
                width: parent.width * 0.75
//                anchors.leftMargin: 10
                anchors.left: number.right
            }
        }
    }
}
