<!DOCTYPE html>
<html>
<head>
    <title>W2UI Demo: form/3</title>
    <link rel="stylesheet" type="text/css" href="css/w2ui-1.5.css"/>
    <script language="JavaScript" src="js/w2ui-1.5.js"></script>
</head>
<body>

<div id="form" style="width: 750px;"></div>

<script type="module">



let form = new w2form({
    box: '#form',
    name: 'form',
    url: '/',
    header: 'Форма1',
    fields: [
        { field: 'textarea', type: 'textarea',
            html: { label: 'Тема', attr: 'style="width: 400px; height: 30px; resize: none"' }
        },
        

        { field: 'textarea2', type: 'textarea',
            html: { label: 'Текст', attr: 'style="width: 400px; height: 60px; resize: none"' }
        },

        { field: 'file', type: 'file',
            html: { label: 'Файлы', attr: 'style="width: 400px;height: 60px"' },
            options: { maxHeight: 100 }
        }
    ],


  actions: {
		"save": function (target, data) { this.submit(); },
		"reset": function (target, data) { this.clear(); },
	
    }
});
</script>

</body>
</html>


        Save() {
                this.save();
