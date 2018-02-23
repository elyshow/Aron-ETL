$(function() {
	$(".type").combobox({
		valueField: 'value',
		textField: 'text',
		data: [{
			"value": 1,
			"text": "普通文件"
		}, {
			"value": 2,
			"text": "数据库文件"
		}, {
			"value": 3,
			"text": "数据接口"
		}, {
			"value": 4,
			"text": "API 接口-GET"
		}],
	});

	
	$(".meanWordCombobox").combobox({   //表示词
		   onBeforeLoad: function(param){
		      param.type = 1;
	       },
			url:'/standardIndex/comboboxData/',
			textField:'cn_name',
			valueField:'value',
	});
	$(".measurementUnitCombobox").combobox({   //计量单位
		    onBeforeLoad: function(param){
		      param.type = 2;
	       },
			url:'/standardIndex/comboboxData/',
			textField:'cn_name',
			valueField:'value',
	});
	$(".dataTypeCombobox").combobox({  //数据类型
		    onBeforeLoad: function(param){
		      param.type = 3;
	       },
			url:'/standardIndex/comboboxData/',
			textField:'cn_name',
			valueField:'value',
	});
     $(".recognizeCombobox").combobox({  //提交机构
		  onBeforeLoad: function(param){
		      param.type = 4;
	       },
			url:'/standardIndex/comboboxData/',
			textField:'recognname',
			valueField:'recognid',
	});

})

$(function(){
    $('#standardRule').tabs({
        clicks:[0,1,2,3,4,5],
        onSelect:function(title,index){
            if($(this).tabs('options').clicks[index] == 0) {
				loadDataList({
					list: '#a_dStandardList',
					url: '/standardIndex/standardData/',
					type: index,
					searchbox:'#tab1SearchBox'
				});
			}
			if($(this).tabs('options').clicks[index] == 1) {
				loadDataList({
					list: '#e_gStandardList',
					url: '/standardIndex/standardData/',
					type: index,
					searchbox:'#tab2SearchBox'
				});
			}
			if($(this).tabs('options').clicks[index] == 2) {
				loadDataList({
					list: '#i_mStandardList',
					url: '/standardIndex/standardData/',
					type: index,
					searchbox:'#tab3SearchBox'
				});
			}
			if($(this).tabs('options').clicks[index] == 3) {
				loadDataList({
					list: '#l_pStandardList',
					url: '/standardIndex/standardData/',
					type: index,
					searchbox:'#tab4SearchBox'
					 
				});
			}
			if($(this).tabs('options').clicks[index] == 4) {

				loadDataList({
					list: '#q_tStandardList',
					url: '/standardIndex/standardData/',
					type: index,
					searchbox:'#tab5SearchBox'
					
				});
		    }
			if($(this).tabs('options').clicks[index] == 5) {
				loadDataList({
					list: '#u_zStandardList',
					url: '/standardIndex/standardData/',
					type: index,
					searchbox:'#standardSearchBox'
					
				});
			}

        }
    }).tabs('unselect', 0).tabs('select', 0)

})


function loadDataList(obj){
	window.list = obj.list
	window.type = obj.type
	//console.log(obj.url)
    $(obj.list).datagrid({
        url:obj.url ,
        queryParams:{
            type: obj.type,
        },
        method:'post',
		striped:true,
		autoRowHeight:true,
        toolbar:obj.toolbar,
        columns:[[
            {field:'checkbox',checkbox:true},
			{field:'cnname',title:'中文名称',width:'15%',},
			{field:'identifier',title:'标识符',width:'15%',},
			{field:'object',title:'对象类',width:'15%',},
			{field:'datatype',title:'数据类型',width:'7%',
			formatter:function (value,row,index) {
				if (value == 'string') {
					return "字符型";
				}
				if (value == 'numeric') {
					return "数值型";
				}
				if (value == 'date') {
					return "日期型";
				}
				if (value == 'datetime') {
					return "日期时间型";
				}
				if (value == 'time') {
					return "时间型";
				}
				if (value == 'bool') {
					return "布尔型";
				}
				if (value == 'binary') {
					return "二进制型";
				}

			}
			},
			{field:'standardsou',title:'数据源',width:'15%',},
			{field:'state',title:'标准来源',width:'10%',formatter:function (v, r, i) {
                if(v == 2){
                    return '内部标准'
                }else{
                    return '外部标准'
                }
            }},

			{field:'oper',title:'操作',width:'20%',formatter:dataBut},
        ]],
		onLoadSuccess:function(){
            $('.stateEditor').linkbutton({
					iconCls: 'icon-edit',
				});
				$('.stateDetail').linkbutton({
					iconCls: 'icon-more'
				});
				stateButton(obj.list)
        },

    });

	 $(obj.searchbox).searchbox({
        prompt:'请输入标识符搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $(obj.list).datagrid('load', {condition:v,type:obj.type});
			console.log(v);
			console.log('111');
        }
    })

	//提交机构信息选择

	$("#chooseRecognize").datagrid({
		url:'/standardIndex/recognizeData/',
		fitColumns:true,
		rownumbers:true,
		singleSelect:true,
		toolbar:'#choose',
		columns:[[
			{field:'checkbox',checkbox:true},
			{field:'codename',title:'标准代码名称',width:'30%',},
			{field:'codetable',title:'标准代码表',width:'30%',},
			{field:'datasource',title:'标准数据源',width:'30%',},
		]]
	});

	$('#infoSearchBox').searchbox({
        prompt:'请输入标准代码表搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#chooseRecognize').datagrid('load', {condition:v});
			console.log(v);
			console.log('111');
        }
    })

}

function stateButton(list){
    var dataAll = $(list).datagrid('getSelected');
}


function dataBut(value,r,index){
	  return '<a data-hover="编辑" title="编辑" class="stateEditor" href="javascript:editStandardData(' + index + ');"  data-options="" style="margin:8px 5px;"></a>'+' '+
			'<a data-hover="详情" title="详情" class="stateDetail" href="javascript:detailStandard(' + index + ');" data-options="" style="margin:8px 5px;"></a>'

}

//编辑信息
function editStandardData(index) {
	    $('input[name="save_type"]').val('edit')
        var data_identi = $(list).datagrid('getRows')[index];
	    console.log(data_identi.identifier);
		if(data_identi != undefined){
			$('#insideIdenti').validatebox({
				novalidate:true,
			});
		}

        linkbutton_click('open_dialog', {dialog:'#standardDialog'});
			$.post('/standardIndex/Detail/', {data: data_identi.identifier}, function (ret) {
				$(".recognizeCombobox").combobox("select", ret[0].sub_recogn); //获取数据到input框
				$(".measurementUnitCombobox").combobox("select", ret[0].meas_unit);
				$(".dataTypeCombobox").combobox("select", ret[0].datatype);
				$(".meanWordCombobox").combobox("select", ret[0].impressword);
				$("#id").val(ret[0].id);
				$("#insideIdenti").val(ret[0].insertIdenti).validatebox('validate');
				
				$("#samilarName").val(ret[0].samilarname);
				$("#object").val(ret[0].object);
				$("#featureWord").val(ret[0].feature);
				$("#dataFormat").val(ret[0].datarule);
				$("#valueRange").val(ret[0].valuerange);
				$("#draftsman").val(ret[0].main_writer);
				$("#definedIntro").val(ret[0].introduce);
				$("#approvedDate").val(ret[0].approve_date);
				$("#quotdStandard").val(ret[0].datafrom);
				$("#version").val(ret[0].version);
				$("#cn_spell").val(ret[0].cn_spell);
				$("#remark").val(ret[0].remark);
				$("#chineseName").val(ret[0].cn_name);
				$("#saveTypeFile").val(ret[0].state);
				$("#identifier").val(ret[0].identi).validatebox('validate');
				$("#relation").val(ret[0].relation);
			})
}

function detailStandard(index) {
        var data_identi = $(list).datagrid('getRows')[index];
	    console.log(data_identi.identifier);
	    console.log(identifier)
        linkbutton_click('open_dialog', {dialog:'#detailStandardDialog'});
			$.post('/standardIndex/Detail/', {data: data_identi.identifier}, function (ret) {
				$(".Rule").each(function () {
					console.log(ret)
					if($(this).val()==ret[0].rule)
						$(this).attr('checked',true);
				});
				$(".recognizeCombobox").combobox("select", ret[0].sub_recogn); //获取数据到input框
				$(".measurementUnitCombobox").combobox("select", ret[0].meas_unit);
				$(".dataTypeCombobox").combobox("select", ret[0].datatype);
				$(".meanWordCombobox").combobox("select", ret[0].impressword);
				$("#insideIdentiDetail").val(ret[0].insertIdenti);
				$("#samilarNameDetail").val(ret[0].samilarname);
				$("#objectDetail").val(ret[0].object);
				$("#featureWordDetail").val(ret[0].feature);
				$("#dataFormatDetail").val(ret[0].datatype);
				$("#sfileNameWayDetail").val(ret[0].datarule);
				$("#valueRangeDetail").val(ret[0].valuerange);
				$("#draftsmanDetail").val(ret[0].main_writer);
				$("#definedIntroDetail").val(ret[0].introduce);
				$("#approvedDateDetail").val(ret[0].approve_date);
				$("#quotdStandardDetail").val(ret[0].datafrom);
				$("#versionDetail").val(ret[0].version);
				$("#cn_spellDetail").val(ret[0].cn_spell);
				$("#remarkDetail").val(ret[0].remark);
				$("#chineseNameDetail").val(ret[0].cn_name);
				$("#saveTypeFileDetail").val(ret[0].state);
				$("#identifierDetail").val(ret[0].identi);
				$("#relationDetail").val(ret[0].relation);
			}, 'json')
}

function closeDetail() {
	$('#detailStandardDialog').dialog('close');
}
function cancel() {
	$('#standardDialog').dialog('close');

}

function standardAdd(){
	$('input[name="save_type"]').val('add')
	   $('#standardDataForm').form('reset');
	    linkbutton_click('open_dialog' ,{dialog: '#standardDialog'});
}

function sub_data() {
    console.log(type)
	$("#standardDataForm").form('submit', {
		url:'/standardIndex/addStandardData/',
		onSubmit: function () {
			console.log($(this).form('validate'))
			return $(this).form('validate');
		},
		success: function (data) {
			$('#standardDialog').dialog('close');
			$('#a_dStandardList').datagrid('reload');
			$('#e_gStandardList').datagrid('reload');
			$('#i_mStandardList').datagrid('reload');
			$('#l_pStandardList').datagrid('reload');
			$('#q_tStandardList').datagrid('reload');
			$('#u_zStandardList').datagrid('reload');
		}
	});

}

//删除信息
// function standardDel(num){
// console.log(num)
// if(num=='0') {
// 	var data = $("#a_dStandardList").datagrid('getSelections');
//     var list = '#a_dStandardList'
// }
// if(num=='1') {
// 	var data = $("#e_gStandardList").datagrid('getSelections');
// 	var list = '#e_gStandardList'
//
// }
// if(num=='2') {
// 	var data = $("#i_mStandardList").datagrid('getSelections');
// 	var list = '#i_mStandardList'
//
// }
// if(num=='3') {
// 	var data = $("#l_pStandardList").datagrid('getSelections');
// 	var list = '#l_pStandardList'
//
// }
// if(num=='4') {
// 	var data = $("#q_tStandardList").datagrid('getSelections');
// 	var list = '#q_tStandardList'
//
// }
// if(num=='5') {
// 	var data = $("#u_zStandardList").datagrid('getSelections');
// 	var list = '#u_zStandardList'
//
// }
// if(data.length == 0){
// 	$.messager.alert('警告','请选择至少一条数据','warning');
// }
// else
// {
// 	$.messager.confirm('确认删除框', '是否确定删除选中记录?', function (ok) {
// 		if (ok) {
// 			var ids = '';
// 			for (var i in data) {
// 				ids += data[i].id + ',';
// 			}
// 			ids = ids.substr(0, ids.length - 1);
// 			$.get('/standardIndex/delData/', {data: ids}, function (msg) {
// 				$(list).datagrid('reload');
// 			})
// 		}
// 	})
// }
//
// //删除数据
// function delData() {
// 	    var v= $("#del").attr("value")
// 	    standardDel(v)
//
// }
//
// function delData1() {
// 	    var v= $("#del1").attr("value")
// 	    standardDel(v)
//
// }
//
// function delData2() {
// 	    var v= $("#del2").attr("value")
// 	    standardDel(v)
//
// }
// function delData3() {
// 	    var v= $("#del3").attr("value")
// 	    standardDel(v)
//
// }
//
// function delData4() {
// 	    var v= $("#del4").attr("value")
// 	    standardDel(v)
//
// }
// function delData5() {
// 	    var v= $("#del5").attr("value")
// 	    standardDel(v)
//
// }


function delData() {
	console.log(type)
	var nowlist;
	switch (type){
		case 0:
			nowlist = $('#a_dStandardList');
			break;
		case 1:
			nowlist = $('#e_hStandardList');
			break;
		case 2:
			nowlist = $('#i_mStandardList');
			break;
		case 3:
			nowlist = $('#l_pStandardList');
			break;
		case 4:
			nowlist = $('#q_tStandardList');
			break;
		case 5:
			nowlist = $('#u_zStandardList');
			break;
		default:
			return false;
	}

	var data = nowlist.datagrid('getSelections');
	if (data.length == 0) {
		$.messager.alert('警告', '请选择至少一条数据', 'warning');
	}
	else {
		$.messager.confirm('确认删除框', '是否确定删除选中记录?', function (ok) {
			if (ok) {
				var ids = '';
				for (var i in data) {
					ids += data[i].id + ',';
				}
				ids = ids.substr(0, ids.length - 1);
				console.log(ids)
				$.post('/standardIndex/delData/', {data: ids}, function (msg) {
				nowlist.datagrid('reload');
 			})
			}
		})
	}
}

//打开dialog
function recognData() {
    $('#standardFromDialog').dialog('open')
}

function cancelDialog() {
      $('#standardFromDialog').dialog('close');
}

function chooseData() {
	var data = $("#chooseRecognize").datagrid('getSelected');
	$("#quotdStandard").val(data.codetable);
	$('#standardFromDialog').dialog('close')

}

function insetstandrd() {
	$('#standardRule').datagrid({
	     url: "/standardIndex/insertStandard/",
		success: function (data) {
			$("#standardRule").datagrid('reload');
			$("#a_dStandardList").datagrid('reload');
			$("#e_gStandardList").datagrid('reload');
			$("#i_mStandardList").datagrid('reload');
			$("#l_pStandardList").datagrid('reload');
			$("#q_tStandardList").datagrid('reload');
			$("#u_zStandardList").datagrid('reload');
		}

	})

}
// function insetstandrd() {
// 	$("#standardDataForm").form('submit', {
// 		url: "/standardIndex/insertStandard/",
// 		onSubmit: function () {
// 	//		console.log($(this).form('validate'))
// 			return $(this).form('validate');
// 		},
// 		success: function (data) {
// 			$("#standardRule").datagrid('reload');
// 		//	$('#standardDialog').dialog('close');
// 			$('#a_dStandardList').datagrid('reload');
// 			$('#e_gStandardList').datagrid('reload');
// 			$('#i_mStandardList').datagrid('reload');
// 			$('#l_pStandardList').datagrid('reload');
// 			$('#q_tStandardList').datagrid('reload');
// 			$('#u_zStandardList').datagrid('reload');
// 		}
// 	});
//
// }


datagrid=$("#standardRule").datagrid({
	url: "/standardIndex/insertStandard/",


})