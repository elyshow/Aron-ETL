/**
 * Created by Administrator on 2016-08-12.
 */
/*数据总线API*/
$(function(){
	$("#table1").datagrid({
		url:'/dataway/showData/',
		toolbar:'#metToolBar',
		method:'post',
        autoRowHeight:true,
        fit:true,
	columns:[[
		{field:'nameapi',title:'接口名称',align:'center',width:'25%',},
		{field:'idapi',title:'接口ID',align:'center',width:'25%',},
		{field:'createtime',title:'创建时间',align:'center',width:'24.5%',},
		{field:'oper',title:'操作',align:'center',width:'24%',formatter:func},
	]],
        onLoadSuccess:function(){
             // 图标
            $('.detail').linkbutton({
               iconCls: 'icon-search',
            });
			$('.detail111').linkbutton({
               iconCls: 'icon-search',
            });
            $('.test').linkbutton({
               iconCls:'icon-search'
            })
        },
	})
	 $('#metSearchBox').searchbox({
        prompt:'请输入接口名称搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#table1').datagrid('load', {condition:v,type:1});
        }
    })
    $("#datawayfield").datagrid({
        // url: '/dataway/dragData/',
        url: '/dataway/datawayfield/',
        method: 'post',
        columns: [[
            {field: 'field_english', title: '字段英文名', width: '29%',},
            {field: 'field_chinese', title: '字段中文名', width: '39%',},
            {field: 'show_type', title: '数据类型', width: '29%',},
        ]],
    })
    $("#datawaycondition").datagrid({
        url: '/dataway/datawaycondition/',
        method: 'post',
        rownumbers:true,
        columns: [[
            {field: 'field_english', title: '字段英文名', width: '29%',},
            {field: 'field_chinese', title: '字段中文名', width: '35%',},
            {field: 'show_type', title: '数据类型', width: '29%',},
        ]],
    })
    $('#datawaycondition').closest('div.datagrid-view').find('div.datagrid-header-rownumber').html('条件顺序')
})

function func(v,r,i){
    console.log(r)
	return  '<a class="detail111" href="javascript:metCheck();" data-option="" style="margin-right:8px">详情</a><a class="test" onclick="testInterface('+r.idapi+')">测试</a>'
}

function testInterface(i){
    window.open('/dataway/csindex/' + i);
}

//查看详情
function metCheck() {
	var row=$("#table1").datagrid('getSelected');
    dataidapi = row.idapi;
    $('#nameapidata').val(row.nameapi);
    $('#idapidata').val(row.idapi);
    $('#createtimedata').val(row.createtime);
    $('#warehouseapidata').val(row.warehouseapi);
    $('#tableapidata').val(row.tableapi);
    linkbutton_click('open_dialog',{dialog:'#cheDialog'});
    $("#datawayfield").datagrid('load', {'dataidapi': dataidapi});
    $("#datawaycondition").datagrid('load', {'dataidapi': dataidapi});
}
//关闭详情页
function che() {
	$("#cheDialog").dialog('close');
	$("#table1").datagrid('reload');
}
//前台删除方法
function metDel() {
	var data = $("#table1").datagrid('getSelections');
	if(data.length == 0){
		$.messager.alert('警告','请至少选择一条数据','warning');
		// return false;
	}
	else{
	$.messager.confirm('确认删除框','是否确定删除选中记录?',function(ok){
		if(ok){
			var ids = '';
			for (var i in data){
				ids += data[i].idapi + ',';
			}
			ids = ids.substr(0, ids.length -1);
			$.get('/dataway/delData/',{data:ids},function(msg){
				$("#table1").datagrid('reload');
			})
		}
	})
		}
}

//前台修改方法
function changeMet() {
	var row=$("#table1").datagrid('getSelections');
	if(row.length==0||row.length>1) {
		$.messager.confirm('警告', '请选择一条数据', 'warning');
	}
		else{
		linkbutton_click('open_dialog',{dialog:'#metDialog'});
        $('#apiName').val(row[0].nameapi);
        $('#idapi22').val(row[0].idapi);
        $("#table1").datagrid('reload');
        console.log(row[0].idapi)

	}
}
//前台修改并保存方法
// function changesave() {
// 	// console.log(222)
// 	$('#change_list').form('submit', {
// 		url: "/dataway/changeMet/",
// 		onSubmit: function () {
// 			return true
// 		},
// 		success: function (data) {
// 			$('#changeMet').dialog('close');
// 			$('#table1').datagrid('reload');
// 		}
// 	});
// }







/*新增接口*/

$(function() {
   $("#mylist1").datagrid({
        url: urls['getUnRegisterDataList'],
        method:'post',
        toolbar:'#cleanRulesToolBar',
        onSelect:checkButton,
        onSelectAll:checkButton,
        onUnselect:checkButton,
        onUnselectAll:checkButton,
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'table_chinese', title: '资源表名', width: '35%',},
            {field: 'source', title: '数据来源', width: '35%',},
            {field: 'oper', title: '操作', width: '28%',formatter:operationCleaningRules},
        ]],
        onLoadSuccess:function(){
            //$.parser.parse();
            $('.cjm').linkbutton();
            checkButton()
        },
    });
	$('#treeList').treegrid({
	url: urls['getResourceTreeData'],
	idField:'id',
	treeField:'text',
	fit:true,
	onClickRow:function(row){
		domData()
	},
	columns:[[
		{title:'来源库',field:'text',width:200},
		{field:'id',title:'id',width:'0%',align:'center',hidden:'true'},
	]],
    });
   $('#dataTbas').tabs('disableTab', 1);
   $('#dataTbas').tabs('disableTab', 2);
})
function domData() {
//双击事件获取行中的数据id
	var data = $("#treeList").treegrid('getSelected');
	dataid = data.id;
//局部刷新datagrid区域
    $("#mylist1").datagrid('load', {'dataid': dataid});
}

function nextTab1(){
    $('#dataTbas').tabs('enableTab', 1);
    $('#dataTbas').tabs('select', 1);
}

function nextDataway2(){
    $('#dataTbas').tabs('enableTab', 2);
    $('#dataTbas').tabs('select', 2);
    $("#drag6").datagrid('load', {'dataid': 0});
    // var tabledata = $('#mylist1').datagrid('getSelections');
}


$(function() {
    $('#drag5').treegrid({
        url: '/cataloguedataway/getData/',
        method: 'post',
        idField:'id',
        fit:true,
        treeField:'cataloguename',
        columns:[[
            {field: 'checkbox', checkbox: true},
            {title:'目录名',field:'cataloguename',width:215},
            {field: 'id', title: '目录编号', width: 110},
        ]],
    })
    $("#drag6").datagrid({
        method: 'post',
        url: '/cataloguedataway/allData/',
        pagination:false,
        fit:true,
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'cataloguename', title: '目录名', width: 215},
            {field: 'id', title: '目录编号', width: 110}
        ]],
    });
     $('#dataTbas').tabs('disableTab', 1);
     $('#dataTbas').tabs('disableTab', 2);
     $('#dataTbas').tabs('disableTab', 3);
})

function nextDataway3(){
    $('#dataTbas').tabs('enableTab', 3);
    $('#dataTbas').tabs('select', 3);
    var row = $('#drag2').datagrid('getSelections');
    for (var i in row){
        $('#mylist_condition').datagrid('appendRow',row[i]);
    }
    // var catalogue = $('#drag6').datagrid('getRows');

    // console.log(row)
    //获取来源表数据
    //jquery获取input输入值方法

    var idapi33 = $('#idapi22').val();
       //获取dialog某一个列表中的数据
    // var warehouse = $('#treeList').treegrid('getSelected');
    // console.log(warehouse)
        //将第一个tab中选中的数据传到最后一个tab里
    $('#APIName').val(apidata);
    $('#idapi11').val(idapi33);
    // $('#catalogueTypeid').val(catalogue.id);
    // $('#catalogueName').val(ids);

    // $('#mylist_condition').datagrid('appendRow',row);
    	$("#cleaningRulesForm2").form('submit', {
		url: "/^dataway/catalogue/",
        method: 'post',
		onSubmit: function (p) {
            var rowsData = $('#drag6').datagrid('getRows');
			var ids = '';
			for (var i in rowsData) {
				ids += rowsData[i].id + ',';
			}
			p.ids =ids.substr(0, ids.length - 1);
			return true
		},
	});
}


//取消
function remove(){
    $('#metDialog').dialog('close');
}
//增加
function adddataway(){
    var rowsData1 = $('#drag4').datagrid('getRows');
    console.log(rowsData1)
    var json1 =JSON.stringify(rowsData1);
    console.log(json1)
    var rowsData2 = $('#mylist_condition').datagrid('getRows');
    console.log(rowsData2)
    var json2 =JSON.stringify(rowsData2);
    console.log(json2)
    var rowsData3 = $('#drag6').datagrid('getRows');
    console.log(888888888)
    console.log(rowsData3)
    var json3 =JSON.stringify(rowsData3);
    console.log(json3)
    // var rowsData3 = $('#drag6').datagrid('getRows');
    // console.log(rowsData3)
    // var json3 =JSON.stringify(rowsData3);
    // console.log(json2)
    // var ids = [{"typeid":rowsData[i].id}];
    // console.log(ids)
    // for (var i in rowsData) {
    //     ids += rowsData[i].id + ',';
    //     console.log(ids)
    // }
    // ids = ids.substr(0, ids.length -1);
    // console.log(ids)
    // p.ids =ids.substr(0, ids.length - 1);
    // p.ids =ids.substr(0, ids.length - 1);
    $().linkbutton('saveChange', {
    form:'#datawayForm',
    dialog:'#metDialog',
    url:'/dataway/saveData/',
    param:{
        hierarchy1: json1,
        hierarchy2: json2,
        hierarchy3: json3,
    },
    });
    $('#table1').datagrid('reload');
}


// 接口配置设置字段
$(function() {
    $("#drag1").datagrid({
        url: '/dataway/dragData/',
        pagination: false,
        method: 'post',
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'field_english', title: '字段英文名', width: '29%',},
            {field: 'field_chinese', title: '字段中文名', width: '39%',},
            {field: 'show_type', title: '数据类型', width: '29%',},
        ]],
    }),
    $(".drag2").datagrid({
        url: '/dataway/dragData/',
        pagination: false,
        method: 'post',
        columns: [[
            {field: 'checkbox', checkbox: true},
            {field: 'field_english', title: '字段英文名', width: '29%',},
            {field: 'field_chinese', title: '字段中文名', width: '39%',},
            {field: 'show_type', title: '数据类型', width: '29%',},
        ]],
    }),
    $('#dataTbas').tabs('disableTab', 2);
	// $('#dataTbas').tabs('select', 1);
})
//拖拽方法
function leftToRight(leftToRight, oneOrMore){
    var leftList = $('#drag1'),rightList = $('.drag2'),l = r = '';
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
        var dataid = document.getElementById("dataid22").value
        r.datagrid('load',{"dataid":dataid});
       // l.datagrid('loadData',[]);
    }
}

//编目
function leftToRight2(leftToRight2, oneOrMore2){
    var leftList = $('#drag5'),rightList = $('#drag6'),l = r = '';
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
        l.treegrid('getData','/cataloguedataway/getData/');
        $('#drag5').treegrid('reload');
    }
}

function checkButton(){
    var list = $('#mylist1').datagrid('getSelections');
    if(list.length == 0){
        $('#editCleaningRulesBtn').linkbutton('disable')
    }else if(list.length > 1 ){
        $('#editCleaningRulesBtn').linkbutton('disable')
    }else{
        $('#editCleaningRulesBtn').linkbutton('enable')
    }
}


function operationCleaningRules(value,row,index) {
    return '<a class="easyui-linkbutton cjm" onclick="nextDataway('+index+')" data-options="iconCls:\'icon-edit\'" style="margin-left: 30px;" >下一步</a>'
}


//第一个选项卡，下一步按钮
function nextDataway(i){
    //获取按钮选中的行
    var data = $('#mylist1').datagrid('getRows')[i]
    //获取输入框中的api名字
    var apidata = $('#apiName').val();
    //此行对应的id，用来查询下一个表的相应数据
    dataid = data.table_id;
    console.log(dataid)
    //通过id关联drag1，刷出相应数据
    $("#drag1").datagrid('load', {'dataid': dataid});
    //将id传到最终确认界面
    $('#dataid22').val(dataid);
    //将来源表传到最终确认界面
    $('#warehouseName').val(data.source);
    //将来源表传到最终确认界面
    $('#tableName').val(data.table_chinese);
    //将api名称传到最终确认界面
    $('#APIName').val(apidata);
    //启用第二个选项卡
    $('#dataTbas').tabs('enableTab', 1);
    //跳转到第二个选项卡
    $('#dataTbas').tabs('select', 1);
}





// 确认接口配置
$(function() {
    $(".drag2").datagrid({
    method: 'post',
    columns: [[
        {field: 'checkbox', checkbox: true},
        {field: 'field_english', title: '字段英文名', width: '29%',},
        {field: 'field_chinese', title: '字段中文名', width: '39%',},
        {field: 'show_type', title: '数据类型', width: '29%',},
    ]],
    })
    $("#mylist_condition").datagrid({
        // url: '/dataway/conditionData/',
        method: 'post',
        rownumbers:true,
        columns: [[
            {field: 'field_english', title: '字段英文名', width: '29%',},
            {field: 'field_chinese', title: '字段中文名', width: '34%',},
            {field: 'show_type', title: '数据类型', width: '29%',},
        ]],
    }),
     $('#mylist_condition').closest('div.datagrid-view').find('div.datagrid-header-rownumber').html('条件顺序')
})
