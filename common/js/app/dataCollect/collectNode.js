$(function(){
	$("#collectNodeList").datagrid({
		url:urls['getCollectNodeListData'],
		toolbar:'#collectNodeToolBar',
		method:'post',
		autoRowHeight:true,
		striped:true,
		columns:[[
			{field:'checkbox',checkbox:true},
			{field:'id',title:'节点id',width:'10%',hidden:true},
			{field:'collectNodeName',title:'节点名称',width:'25%', showTitle:true },
			{field:'collectNodeRegion', title: '所属区域', width: '25%'},
			{field:'collectNodeStatus',title:'节点状态',width:'25%',},
			{field:'oper',title:'查看任务详情',width:'23%',formatter:operCollectNode},
		]],

		onLoadSuccess:function(){
			$('.detailMore').linkbutton({iconCls: 'icon-more'});
		}
	});

	search('#collectNodeList', '#collectNodeSearchBox');
});


function operCollectNode(v, r, i){
	return '<a class="detailMore" href="javascript:collectNodeDetail('+i+');"  data-options="" style="margin:8px 5px;" data-hover="详情" title="查看详情"></a>'
}


function collectNodeDetail(i){
	var data = getEditData(i, '#collectNodeList');
	if(data == false){
		return;
	}
	//console.log(data);
    window.open(urls['collectTask'] + data.id, '_blank')
    $("#collectNodeList").datagrid('unselectAll')
}

//增加节点弹出框

function addCollectNode() {
    $('#collectNodeDialog').dialog({
        title: '新增采集节点',
        onOpen: function () {
            $('#collectNodeForm').form('reset');
        },
        onClose: function () {
            $("#collectNodeList").datagrid('clearSelections')
        }
    }).dialog('open');
}

function delCollectNode() {
	var data = $("#collectNodeList").datagrid('getSelections');
	if(data.length == 0){
		$.messager.alert('警告','请至少选择一条数据','warning');
		// return false;
	}
	else{
        $.messager.confirm('确认删除框','删除节点会删除节点下的所有任务,是否继续?',function(ok){
            if(ok){
                var ids = '';
                for (var i in data){
                    ids += data[i].id + ',';
                }
                ids = ids.substr(0, ids.length -1);
                $.post(urls['delCollectNode'],{data:ids},function(msg){
                    if(msg.errorCode != '0x0000'){
                        $.messager.alert('错误', msg.errorString, 'error');
                    }
                    $("#collectNodeList").datagrid('reload');
                }, 'json')
            }
        })
	}
}

function editCollectNode() {
    var data = $("#collectNodeList").datagrid('getSelections');
	if(data.length == 0 || data.length > 1){
		$.messager.alert('警告','请选择一条数据','warning');
		// return false;
	}else{
        $('#collectNodeDialog').dialog({
            title: '修改采集节点',
            onOpen: function () {
                $('#collectNodeForm').form('reset');
                $("#collectNodeForm input[name='id']").val(data[0].id);
                $("#collectNodeForm input[name='collectNodeName']").val(data[0].collectNodeName);
                $("#collectNodeForm input[name='collectNodeRegion']").val(data[0].collectNodeRegion);
                $('#collectNodeForm').form('validate');
            },
            onClose: function () {
                $("#collectNodeList").datagrid('clearSelections')
            }
        }).dialog('open');
    }
}


// 保存节点信息
function saveCollectDom(){
    $("#collectNodeForm").form('submit', {
        url: urls['saveCollectNode'],
        onSubmit: function () {
            return $(this).form('validate');
        },
        success: function (msg) {
            msg = $.parseJSON(msg)
            if(msg.errorCode == '0x0000'){
                $('#collectNodeForm').form('reset');
                $("#collectNodeDialog").dialog('close');
                $("#collectNodeList").datagrid('reload');
            }else {
                $.messager.alert('错误', msg.errorString, 'error');
            }
        }
    });
}
