$(function(){
    $('#regAndReleaseTab').tabs({
        onSelect:function(title,index){
            switch(index){
                case 0:
                    //loadTree('unRegisterResourceTreeList', 'unRegisterResourceDataList');
                    loadUnRegisterDataList()
                    break;
                case 1:
                    loadRegisterDataList()
                    break;
                case 2:
                    if($('#publishResourceTreeList').children().length == 0)
                        loadTree('publishResourceTreeList', 'publishResourceDataList');
                    loadPublishResourceDataList()
                    break;
                default:
                    $.messager.alert('错误', '选显卡不存在', 'error');
                    break;
            }
        }
    })
    loadTree('unRegisterResourceTreeList', 'unRegisterResourceDataList');
    loadUnRegisterDataList()

    //为注册对话框绑定相应事件
    saveRegisterResource('saveRegisterBtn', 'unRegisterResourceDialogTab', 'unRegisterResourceForm', 'submitRegisterResource')

    //为发布对话框绑定相应事件
    saveRegisterResource('savePublishBtn', 'registerResourceDialogTab', 'registerResourceForm', 'submitPublishResource')
})


function saveRegisterResource(linkBtnID,tabID,formID,callbackFunc){
    $('#' + linkBtnID).linkbutton({
        value:'next',
        length:0,
        onClick:function(){
            var tabs = $('#' + tabID),
                t = $(this),
                opt = t.linkbutton('options'),
                value = opt.value,
                tab = tabs.tabs('getSelected'),
                index = tabs.tabs('getTabIndex',tab) + 1,
                newTab = tabs.tabs('getTab', index);
                opt.length = tabs.tabs('tabs').length
            if(value == 'next'){
                var validate_input =tab.find('.validatebox-invalid');
                if(validate_input.length != 0){
                    validate_input.eq(0).addClass('textbox-focused').focus().mouseover();
                   // return false;
                }
                if(newTab.panel('options').disabled == true){
                    tabs.tabs('enableTab', index);
                }
                tabs.tabs({
                    onSelect:function(title, index){
                        if(index == opt.length - 1){
                            opt.value = 'save';
                            t.linkbutton({text:'确定'});
                        }else{
                            opt.value = 'next';
                            t.linkbutton({text:'下一步'});
                        }
                    }
                }).tabs('select', index);
            }else{
                window[callbackFunc].call(this,formID);
            }
        }
    })
}


function loadPublishTree(){
    $('#unPublishCatalogList').treegrid({
        method: 'post',
        idField:'id',
        treeField:'text',
        fit:true,
        hasCatalog:{},
        columns:[[
            {title:'目录名',field:'text',width:'75%'},
            {field: 'id', title: '目录编号', width: '20%'},
        ]],
        onLoadSuccess:function(){
            $(this).treegrid('collapseAll');
        }
    })
}

function submitRegisterResource(formID){
    $('#' + formID).form('submit', {
        method:'post',
        onSubmit:function(param){
            var datas = $('#RegisterTableFieldList').datagrid('getRows')
            var json =JSON.stringify(datas);
            param.hierarchy = json;
            return $(this).form('validate');
        },
        success:function (data) {
            data = $.parseJSON(data)
            if(data.errorCode == '0x0000'){
                $('#unRegisterResourceDataList').datagrid('reload')
                $('#unRegisterResourceDialog').dialog('close')
            }else{
                $.messager.alert('错误', '注册资源失败', 'error', function(){
                    $('#unRegisterResourceDialog').dialog('close')
                })
            }
        }
   })
}

function submitPublishResource(formID){
     $('#' + formID).form('submit', {
        method:'post',
        onSubmit:function(param){
            var rowsData = $('#publishCatalogList').datagrid('getRows')
            var ids = '';
			for (var i in rowsData) {
				ids += rowsData[i].id + ',';
			}
            if(ids == ''){
                $.messager.alert('错误', '请至少选择一个目录发布', 'error')
                return false;
            }
            param.ids = ids.substr(0, ids.length - 1);;
            return $(this).form('validate');
        },
        success:function (data) {
            data = $.parseJSON(data)
            if(data.errorCode == '0x0000'){
                $('#registerResourceDataList').datagrid('reload')
                $('#registerResourceDialog').dialog('close')
            }else{
                $.messager.alert('错误', '发布资源失败', 'error', function(){
                    $('#registerResourceDialog').dialog('close')
                })
            }
        }
   })
}


function addUnRegisterResource(i){
    if(i == undefined){
        var data = $('#unRegisterResourceDataList').datagrid('getSelected')
    }else{
        var data =$('#unRegisterResourceDataList').datagrid('getRows')[i]
    }
    initDialog('#unRegisterResourceDialog','#unRegisterResourceDataList', '注册资源', data)
    loadRegisterTableFieldDataList('unRegisterTableFieldList', 'unRegisterTableFieldSearch', 'unRegisterTableFieldToolBar', data.table_id)
    loadRegisterTableFieldDataList('RegisterTableFieldList', 'unRegisterTableFieldSearch', 'unRegisterTableFieldToolBar')
    initTab('unRegisterResourceDialogTab')
    $('#releasetable').val(data.table_english);
}

function initTab(tabID){
    var i = 1;
    $('#' + tabID).tabs('select', 0)
    while($('#' + tabID).tabs('exists', i)){
        $('#' + tabID).tabs('disableTab', i);
        i++;
    }
}

function Publish(type){
    var leftList = $('#unPublishCatalogList'),rightList = $('#publishCatalogList');

    if(type === false){
        var selections = rightList.datagrid('getSelections');
        if(selections.length > 1){
            $.messager.alert('错误', '一次只能移动一条目录', 'error');
            return false;
        }
        if(selections.length == 0){
            $.messager.alert('错误', '请选择一条目录进行移动', 'error');
            return false;
        }
        var selected = rightList.datagrid('getSelected');
        if(selected.typeparentid == 1){
            var node = leftList.treegrid('getRoots'),
            id = node[node.length - 1].id;
            leftList.treegrid('insert',{
                after:id,
                data: selected,
            })
        }else{
            leftList.treegrid('append',{
                parent:selected.typeparentid,
                data: [selected],
            })
        }
        rightList.datagrid('deleteRow',rightList.datagrid('getRowIndex', selected)).dataid('clearSelections')
    }else{
        var selected = leftList.treegrid('getSelected')
        if(selected == null){
            $.messager.alert('错误', '请选择一个目录进行发布', 'error')
            return false;
        }
        if(leftList.treegrid('getChildren', selected.id).length != 0){
            $.messager.confirm('确定', '该目录不是最小目录，是否继续?', function(ok){
                if(ok){
                    leftList.treegrid('remove',selected.id)
                    rightList.datagrid('appendRow', selected);
                }
            })
        }else{
            leftList.treegrid('remove',selected.id)
            rightList.datagrid('appendRow', selected);
        }
    }
}

function addRegisterResource(i){
    if(i == undefined){
        var data = $('#registerResourceDataList').datagrid('getSelected')
    }else{
        var data =$('#registerResourceDataList').datagrid('getRows')[i]
    }
    initDialog('#registerResourceDialog','#registerResourceDataList', '发布资源', data)
    loadPublishTree()
    LoadPublishCatalog('publishCatalogList', 'unRegisterTableFieldSearch', 'unRegisterTableFieldToolBar')
    initTab('registerResourceDialogTab')
}

function LoadPublishCatalog(listID, searchID, toolbar, condition){
    $('#' + listID).datagrid({
        toolbar:'#' + toolbar,
        method: 'post',
        pagination:false,
        columns: [[
            {field: 'checkbox', checkbox: true},
            {title:'目录名',field:'text',width:'68%'},
            {field: 'id', title: '目录编号', width: '20%'},
        ]],
        queryParams:{
            dataid:condition,
        },
        onLoadSuccess:function(){
            search(searchID, listID);
        }
    })
}

function cancelRegisterResource(i){
    if(i == undefined){
        var data = $('#registerResourceDataList').datagrid('getSelections')
    }else{
        var row = $('#registerResourceDataList').datagrid('getRows')[i],data = [];
        data.push(row)
    }
    $.messager.confirm('确认删除框','是否确定取消发布?',function(ok){
		if(ok){
			var ids = '';
			for (var i in data){
				ids += data[i].resourceid + ',';
			}
			ids = ids.substr(0, ids.length -1);
			 $.get(urls.remokeRegisterResource, {data: ids}, function (msg) {
                    $("#registerResourceDataList").datagrid('reload');
                })
		}
	})
}

function cancelPublishResource(i){
    if(i == undefined){
        var data = $('#publishResourceDataList').datagrid('getSelections')
    }else{
        var row = $('#publishResourceDataList').datagrid('getRows')[i],data = [];
        data.push(row)
    }
    $.messager.confirm('确认删除框','是否确定取消发布?',function(ok){
		if(ok){
			var ids = '';
			for (var i in data){
				ids += data[i].resourceid + ',';
			}
			ids = ids.substr(0, ids.length -1);
			 $.get(urls.remokePublishResource, {data: ids}, function (msg) {
                    $("#publishResourceDataList").datagrid('reload');
                })
		}
	})
}



function leftToRight(leftToRight, oneOrMore){
    var leftList = $('#unRegisterTableFieldList'),rightList = $('#RegisterTableFieldList'),l = r = '';
    if(leftToRight == false){
        l = leftList
        r = rightList
    }else{
        l = rightList;
        r = leftList;
    }

    if(oneOrMore == false){
        var rows = l.datagrid('getSelections');
        if(rows.length == 0){
            $.messager.alert('错误', '请至少选择移动一个字段', 'error');
            return false;
        }
        var index = []
        for(var i = 0; i< rows.length; i++){
            r.datagrid('appendRow',rows[i])
            index.unshift(l.datagrid('getRowIndex',rows[i]))
        }
        for(var i in index)
            l.datagrid('deleteRow',index[i])
    }else{
        l.datagrid('loadData',[])
        var data = $('#unRegisterResourceDataList').datagrid('getSelected')
        r.datagrid('load',l.datagrid('options').queryParams);
        //$('#RegisterTableFieldList').datagrid('load',$('#unRegisterTableFieldList').datagrid('options').queryParams);
    }
}

function loadTree(treeID, dataListID){
    $('#' + treeID).tree({
        //lines:true,
        border:false,
        fit:true,
        onSelect:function(node){
            $('#' + dataListID).datagrid('load',{dataid: node.id});
        },
        onLoadSuccess:function(){
            var root = $(this).tree('getRoots')[0]
            $(this).tree('collapseAll').tree('expand', root.target)
            $(this).tree('select', $(this).tree('getChildren', root.target)[0].target)
        }
    })
}

function loadPublishResourceDataList(){
    $('#publishResourceDataList').datagrid({
        toolbar:'#publishResourceToolbar',
        method:'post',
        onSelect:checkPublishButton,
        onSelectAll:checkPublishButton,
        onUnselect:checkPublishButton,
        onUnselectAll:checkPublishButton,
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'resourceid', title: '资源编号', width: '24%',},
            {field: 'resourcename', title: '资源名称', width: '20%',},
            {field: 'releasetime', title: '发布时间', width: '29%',},
            {field: 'oper', title: '操作', width: '24%',formatter:operationPublish},
        ]],
        onLoadSuccess:function(){
            $('.cancelPublish').linkbutton({iconCls:'icon-edit'});
            checkPublishButton();
            search('publishResourceSearch', 'publishResourceDataList');
        },
    })
}

function loadUnRegisterDataList(){
    $('#unRegisterResourceDataList').datagrid({
        method:'post',
        toolbar:'#unRegisterResourceToolBar',
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'table_chinese', title: '资源表名', width: '35%',},
            {field: 'source', title: '数据来源', width: '35%',},
            {field: 'oper', title: '操作', width: '28%',formatter:operationUnRegister},
        ]],
        onSelect:checkUnRegButton,
        onSelectAll:checkUnRegButton,
        onUnselect:checkUnRegButton,
        onUnselectAll:checkUnRegButton,
        onLoadSuccess:function(){
            $('.unRegisterResource').linkbutton({iconCls:'icon-edit'});
            checkUnRegButton();
            search('unRegisterResourceSearch', 'unRegisterResourceDataList');
        }
    })
}

function loadRegisterDataList(){
    $("#registerResourceDataList").datagrid({
        toolbar:'#registerResourceToolBar',
        method:'post',
        onSelect:checkRegButton,
        onSelectAll:checkRegButton,
        onUnselect:checkRegButton,
        onUnselectAll:checkRegButton,
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'resourceid', title: '注册资源编号', width: '20%',},
            {field: 'resourcename', title: '资源名称', width: '30%',},
            {field: 'registertime', title: '注册时间', width: '25%',},
            {field: 'oper', title: '操作', width: '23%',formatter:operationRegister},
        ]],
        onLoadSuccess:function(){
            $('.publishResource, .cancelRegisterResource').linkbutton({iconCls:'icon-edit'});
            checkRegButton();
            search('registerResourceSearch', 'registerResourceDataList');
        },
    });
}


function loadRegisterTableFieldDataList(listID, searchID, toolbar, condition){
    $('#' + listID).datagrid({
        toolbar:'#' + toolbar,
        method: 'post',
        pagination:false,
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'field_english', title: '字段英文名', width: '20%',},
            {field: 'field_chinese', title: '字段中文名', width: '40%',},
            {field: 'show_type', title: '数据类型', width: '27%',},
        ]],
        queryParams:{
            dataid:condition,
        },
        onLoadSuccess:function(){
            search(searchID, listID);
        }
    })
}

function search(search, list){
    $('#' + search).searchbox({
        prompt:'请输入搜索条件',
        height:24,
        width:200,
        searcher:function(v,n){
            var url = $('#' + list).datagrid('options').url;
            if(url)
                $('#' + list).datagrid('load', {condition:v})
            else {
                $('#' + list).datagrid('checkRow', v);
            }
        }
    })
}

function checkUnRegButton(){
    var list = $('#unRegisterResourceDataList').datagrid('getSelections');
    if(list.length == 0 || list.length > 1){
        $('#addUnRegisterResourceBtn').linkbutton('disable')
    }else{
        $('#addUnRegisterResourceBtn').linkbutton('enable')
    }
}

function checkRegButton(){
    var list = $('#registerResourceDataList').datagrid('getSelections');
    if(list.length == 0 || list.length > 1){
        $('#addRegisterResourceBtn, #cancelRegisterResourceBtn').linkbutton('disable')
    }else{
        $('#addRegisterResourceBtn, #cancelRegisterResourceBtn').linkbutton('enable')
    }
}

function checkPublishButton(){
    var list = $('#publishResourceDataList').datagrid('getSelections');
    if(list.length == 0 || list.length > 1){
        $('#cancelPublishResourceBtn').linkbutton('disable')
    }else{
        $('#cancelPublishResourceBtn').linkbutton('enable')
    }
}

function operationUnRegister(value,row,index){
    return '<a data-hover="注册" title="注册" class="unRegisterResource" onclick="addUnRegisterResource('+index+')" style="margin-left: 70px;"></a>'
}


function operationRegister(value,row,index){
    return '<a data-hover="发布" title="发布" class="publishResource" onclick="addRegisterResource('+index+')" style="margin-right: 5px"></a>' +
           '<a data-hover="取消注册" title="取消注册" class="cancelRegisterResource" onclick="cancelRegisterResource('+index+')" ></a>'
}

function operationPublish(value,row,index){
    return '<a data-hover="取消发布" title="取消发布" class="cancelPublish" href="javascript:cancelPublishResource('+index+');"  style="margin-left: 50px;"></a>'
}
/**
function addCleaningRules(i){
    if(i != undefined){
        var data = $('#mylist1').datagrid('getRows')[i]
         dataid = data.table_id;
         console.log(dataid)
         $("#drag1").datagrid('load', {'dataid': dataid});
         $("#dataid").val(dataid);
    }else{
        var list = $('#mylist1').datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据",'error')
            return false
        }else if(list.length > 1){
            $.messager.alert('错误',"一次只能选择一条数据",'error')
            return false
        }else{
            var data =  $("#mylist1").datagrid('getSelected');
	        dataid = data.table_id;
            $("#drag1").datagrid('load', {'dataid': dataid});
        }
    }
    $('input[name="save_type"]').val('add')
    $('input[name="id"]').val(data.table_chinese)
    $('input[name="releasetable"]').val(data.table_english)
    initDialog('#cleaningRulesDialog','#mylist1' , '注册资源', data);
}


function saveCleaningRules(t){
    var rowsData = $('#drag2').datagrid('getRows');
    var json =JSON.stringify(rowsData);
    $(t).linkbutton('saveChange', {
        form:'#cleaningRulesForm',
        datagrid:'#drag2,#mylist2',
        dialog:'#cleaningRulesDialog',
        url:'/releaseRegisterManagement/saveCleaningRules/',
        param:{
            hierarchy: json,
        },
    })
    // $('#fabuTab').tabs('select',{title:'发布'});
    $('#fabuTab').tabs('select','发布')

}


function saveFabu(t) {
	$("#cleaningRulesForm2").form('submit', {
		url: "/releaseRegister/release/",
		onSubmit: function (p) {
			 var rowsData = $('#drag4').datagrid('getRows');
			var ids = '';
			for (var i in rowsData) {
				ids += rowsData[i].id + ',';
			}
			p.ids =ids.substr(0, ids.length - 1);
			return true
		},
		success: function (data) {
			$('#cleaningRulesDialog2').dialog('close');
			$('#mylist2').datagrid('reload');
			$('#mylist3').datagrid('reload');

		}
	});
     $('#fabuTab').tabs('select','已发布')
}

//获取树
$(function(){
    $('#treeList').treegrid({
        url:'/releaseRegister/getTreeData/',
        idField:'id',
        treeField:'cataloguename',
        onClickRow:function(row){
			domData()
        },
        columns:[[
            {title:'目录结构',field:'cataloguename',width:160},
            {field:'id',title:'id',width:'0%',align:'center',hidden:'true'},
        ]],
    });
})

function domData() {
//双击事件获取行中的数据id
	var data = $("#treeList").treegrid('getSelected');
	dataid = data.id;
    console.log(dataid)
//局部刷新datagrid区域
    $("#mylist1").datagrid('load', {'dataid': dataid});

}

//拖拽
$(function() {
    $("#drag1").datagrid({
        url: '/releaseRegister/dragData/',
        method: 'post',
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'field_english', title: '字段英文名', width: '29%',},
            {field: 'field_chinese', title: '字段中文名', width: '39%',},
            {field: 'show_type', title: '数据类型', width: '29%',},
        ]],
    })
    $("#drag2").datagrid({
        method: 'post',
        url:'/releaseRegister/dragData/',
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'field_english', title: '字段英文名', width: '29%',},
            {field: 'field_chinese', title: '字段中文名', width: '39%',},
            {field: 'show_type', title: '数据类型', width: '29%',},
        ]],
    })
})

$(function() {
   $("#mylist2").datagrid({
        url:'/releaseRegister/registerIndex/',
        method:'post',

        onSelect:checkButton2,
        onSelectAll:checkButton2,
        onUnselect:checkButton2,
        onUnselectAll:checkButton2,
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'resourceid', title: '注册资源编号', width: '20%',},
            {field: 'resourcename', title: '资源名称', width: '20%',},
            {field: 'registertime', title: '注册时间', width: '25%',},
            {field: 'oper', title: '操作', width: '32%',formatter:operationRelease},
        ]],
        onLoadSuccess:function(){
            //$.parser.parse();
            $('.cjm2').linkbutton();
            checkButton2()
        },
    });
   $('#dataCleaningSearch2').searchbox({
        prompt:'请输入资源名称搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#mylist2').datagrid('load', {condition:v})
        }
   })
})


function checkButton2(){
    var list = $('#mylist2').datagrid('getSelections');
    if(list.length == 0){
        $('#addCleaningRulesBtn2').linkbutton('disable')
        $('#revokeCleaningRulesBtn2').linkbutton('disable')
    }else if(list.length > 1 ){
        $('#addCleaningRulesBtn2').linkbutton('disable')
        $('#revokeCleaningRulesBtn2').linkbutton('enable')
    }else{
        $('#addCleaningRulesBtn2').linkbutton('enable')
        $('#revokeCleaningRulesBtn2').linkbutton('enable')
    }
}


function operationRelease(value,row,index) {
    return '<a class="easyui-linkbutton cjm2" onclick="addCleaningRules2('+index+')" data-options="iconCls:\'icon-edit\'" style="margin-left: 23px;">发布</a>' +
           '<a class="easyui-linkbutton cjm2" onclick="revokeRegister('+index+')" data-options="iconCls:\'icon-edit\'" style="margin-left: 23px;">取消注册</a>'
}

function addCleaningRules2(i){
    if(i != undefined){
        var data = $('#mylist2').datagrid('getRows')[i]
    }else{
        var list = $('#mylist2').datagrid('getSelections');
        if(list.length == 0){
            $.messager.alert('错误',"请至少选择一条数据",'error')
            return false
        }else if(list.length > 1){
            $.messager.alert('错误',"一次只能选择一条数据",'error')
            return false
        }else{
            var data =  $("#mylist2").datagrid('getSelected');
        }
    }
    $('input[name="save_type"]').val('add')
    $('input[name="id"]').val(data.table_id)
    initDialog('#cleaningRulesDialog2','#mylist2' , '发布资源', data);
}


$(function() {
      $('#drag5').treegrid({
        url: '/catalogueManagement/getData/',
        method: 'post',
        idField:'id',
        treeField:'cataloguename',
        columns:[[
            {title:'目录名',field:'cataloguename',width:220},
            {field: 'id', title: '目录编号', width: 114},
        ]],
    })
    $("#drag4").datagrid({
        method: 'post',
        url: '/catalogueManagement/allData/',
        fit:false,
        pagination:false,
        width:360,
        height:290,
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'cataloguename', title: '目录名', width: '40%'},
            {field: 'id', title: '目录编号', width: '40%'}
        ]],
    })
})


//取消注册
function revokeRegister() {
    var data = $("#mylist2").datagrid('getSelections');
    console.log(111)
    // if (data.length == 0) {
    //     $.messager.alert('警告', '请至少选择一条数据', 'warning');
    //     // return false;
    // }

    $.messager.confirm('确认取消注册', '是否确定取消注册?', function (ok) {
        if (ok) {
            var ids = '';
            for (var i in data) {
                ids += data[i].resourceid + ',';
            }
            ids = ids.substr(0, ids.length - 1);
            $.get('/releaseRegister/registerCancel/', {data: ids}, function (msg) {
                $("#mylist2").datagrid('reload');
            })
        }
    })



}
// 拖拽方法
function leftToRight(leftToRight, oneOrMore){
    var leftList = $('#drag1'),rightList = $('#drag2'),l = r = '';
    if(leftToRight == false){
        l = leftList
        r = rightList
    }else{
        l = rightList;
        r = leftList;
    }

    if(oneOrMore == false){
        var row = l.datagrid('getSelected');
        if(row == null){
            $.messager.alert('错误', '请至少选择移动一个字段', 'error');
            return false;
        }
        var index = l.datagrid('getRowIndex',row)
        l.datagrid('deleteRow',index)
        r.datagrid('appendRow',row)
    }else{
        l.datagrid('loadData',[])
        var dataid = document.getElementById("dataid").value
        r.datagrid('load',{'dataid': dataid});
       // l.datagrid('loadData',[]);
    }
}


// 拖拽方法2
function leftToRight2(leftToRight2, oneOrMore2){
    var leftList = $('#drag5'),rightList = $('#drag4'),l = r = '';
    l = leftList;
    r = rightList;
    if(leftToRight2 == false && oneOrMore2 == false){
        var row = l.treegrid('getSelected');
        if(row == null){
            $.messager.alert('错误', '请至少选择移动一个字段', 'error');
            return false;
        }
        var index = l.treegrid('getRowIndex',row)
        l.treegrid('remove',row.id)
        console.log(row)
        r.datagrid('appendRow',row)
    }
    if(leftToRight2 == true && oneOrMore2 == false){
        var row2 = r.datagrid('getSelected');
        if(row2 == null){
            $.messager.alert('错误', '请至少选择移动一个字段', 'error');
            return false;
        }
        var index2 = r.datagrid('getRowIndex',row2);
        r.datagrid('deleteRow',index2);
        l.treegrid('append',{parent: row2.typeparentid,data:[{id:row2.id,cataloguename:row2.cataloguename}]})
        $('#drag5').treegrid('reload');
    }
    if(leftToRight2 == false && oneOrMore2 == true){
        l.treegrid('loadData',[]);
        r.datagrid('load',{"dataid":111});
    }
    if(leftToRight2 == true && oneOrMore2 == true){
        r.datagrid('loadData',[]);
        l.treegrid('getData','/catalogueManagement/getData/');
        $('#drag5').treegrid('reload');
    }
}

$(function() {
   $("#mylist3").datagrid({
        url:'/releaseRegister/releaseIndex/',
        method:'post',
        onSelect:checkButton3,
        onSelectAll:checkButton3,
        onUnselect:checkButton3,
        onUnselectAll:checkButton3,
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'resourceid', title: '资源编号', width: '24%',},
            {field: 'resourcename', title: '资源名称', width: '20%',},
            {field: 'releasetime', title: '发布时间', width: '29%',},
            {field: 'oper', title: '操作', width: '24%',formatter:release},
        ]],
        onLoadSuccess:function(){
            //$.parser.parse();
            $('.cjm3').linkbutton();
            checkButton3()
        },
    });
   $('#dataCleaningSearch3').searchbox({
        prompt:'请输入资源名称搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#mylist3').datagrid('load', {condition:v})
        }
   })
})

function checkButton3(){
    var list = $('#mylist3').datagrid('getSelections');
    if(list.length == 0){
        $('#editCleaningRulesBtn3').linkbutton('disable')
    }else if(list.length > 1 ){
        $('#editCleaningRulesBtn3').linkbutton('disable')
    }else{
        $('#editCleaningRulesBtn3').linkbutton('enable')
    }
}


function release(value,row,index) {
    return '<a class="easyui-linkbutton cjm3" href="javascript:fabuCancel();" data-options="iconCls:\'icon-edit\'" style="margin-left: 50px;">取消发布</a>'
}


function fabuCancel(i){
	var data = $("#mylist3").datagrid('getSelections');

	$.messager.confirm('确认删除框','是否确定取消发布?',function(ok){
		if(ok){
			var ids = '';
			for (var i in data){
				ids += data[i].resourceid + ',';
			}
			ids = ids.substr(0, ids.length -1);

			 $.get('/releaseRegister/fabuCancel/', {data: ids}, function (msg) {
                    $("#mylist3").datagrid('reload');
                    $("#mylist2").datagrid('reload');
                })
		}
	})
}



//已发布获取树
$(function(){
    $('#treeList3').treegrid({
        url:'/catalogueManagement/getData/',
        idField:'id',
        treeField:'cataloguename',
        onLoadSuccess:function(){
            console.log(1)
        },
        onClickRow:function(row){
			domData2()
        },
        columns:[[
            {title:'目录结构',field:'cataloguename',width:160},
            {field:'id',title:'id',width:'0%',align:'center',hidden:'true'},
        ]],
    });
})

function domData2() {
//双击事件获取行中的数据id
	var data = $("#treeList3").treegrid('getSelected');
	dataid = data.id;
    console.log(dataid)
//局部刷新datagrid区域
    $("#mylist3").datagrid('load', {'dataid': dataid});

}
*/