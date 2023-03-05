OrgChart.templates.childrenTemplate = Object.assign({}, OrgChart.templates.ana);
OrgChart.templates.childrenTemplate.size = [250, 120];
OrgChart.templates.childrenTemplate.field_0 =
    '<text data-width="230" style="font-size: 18px;" fill="#ffffff" x="125" y="90" text-anchor="middle" class="field_0">{val}</text>';
OrgChart.templates.ana.field_1 =
    '<text width="130" text-overflow="multiline" style="font-size: 14px;" fill="#ffffff" x="230" y="30" text-anchor="end" class="field_1">{val}</text>';
OrgChart.templates.childrenTemplate.field_1 =
    '<text width="130" text-overflow="multiline" style="font-size: 14px;" fill="#ffffff" x="230" y="30" text-anchor="end" class="field_1">{val}</text>';

var chart = new OrgChart(document.getElementById("tree"), {
    mode: "dark",
    min: true,
    menu: {
        pdf: {
            text: "Export PDF"
        },
        png: {
            text: "Export PNG"
        },
    },
    editForm: {
        readOnly: true
    },
    scaleInitial: OrgChart.match.width,
    nodeBinding: {
        field_0: "name",
        field_1: "parent",
        img_0: "img",
    },
    tags: {
        childrenTemplate: {
            template: "childrenTemplate"
        }
    }
});

async function getData() {
    const static_url = url;
    try {
        let res = await fetch(static_url);
        return await res.json();
    } catch (error) {
        alert("Ooops! Something's gone wrong. Please, try again.");
    }
}
async function exec() {
    let nodes = await getData();
    chart.load(nodes);
}

exec();