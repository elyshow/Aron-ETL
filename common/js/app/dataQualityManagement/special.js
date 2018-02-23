// /**
//  * Created by Administrator on 2016-08-12.
//  */
// /*第4个选项卡*/
// $(function(){
// 	$("#table4").datagrid({
// 		url:'/table4/showData4/',
// 		toolbar:'#speToolBar',
// 		method:'post',
//          autoRowHeight:true,
// 		columns:[[
// 			{field:'checkbox',checkbox:true},
//             {field:'schemename',title:'方案名称',width:'20%',align:'center'},
//             {field:'schemetype',title:'方案类型',width:'15%',align:'center'},
//             {field:'checkobject',title:'校验对象',width:'10%',align:'center'},
//             {field:'businesspolice',title:'业务警种',width:'10%',align:'center'},
//             {field:'scheduletime',title:'调度时间',width:'15%',align:'center'},
// 			{field:'oper',title:'查看',align:'center',width:'30%',formatter:func4},
// 		]],  onLoadSuccess:function(){
//              // 图标
//             $('.detail4').linkbutton({
//                iconCls: 'icon-search',
//             });
//     },
// 	})
// 	 $("#combobox_type41").combobox({
//         width:130,
//         valueField:'id',
//         textField:"text",
//         data:[{
//             "id": 1,
//             "text": "全部"
//         }, {
//             "id": 2,
//             "text": "治安"
//         }, {
//             "id": 3,
//             "text": "刑侦"
//         }, {
//             "id": 4,
//             "text": "国保"
//         },{
//             "id":5,
//             "text":"经侦"
//         },{
//             "id":6,
//             "text":"网监"
//         }
//         ],
//     })
// 	 $("#combobox_type42").combobox({
//         width:130,
//         valueField:'id',
//         textField:"text",
//         data:[{
//             "id": 1,
//             "text": "全部"
//         }, {
//             "id": 2,
//             "text": "表间逻辑校验"
//         }, {
//             "id":3,
//             "text":"其他"
//         }
//         ],
//     })
//
// 	 $('#speSearchBox').searchbox({
//         prompt:'请输入方案名称搜索',
//         height:24,
//         width:200,
//         searcher:function(v,n){
//            $('#table4').datagrid('load', {condition:v,type:1});
// 			console.log(v);
// 			console.log('111');
//         }
//     })
//
// })
//
//
// function func4(v,r,i){
// 	return  '<a class="detail4" href="javascript:speDetail();" data-option="">查看详情</a>'
// }
//
//
// //前台详情方法
// function speDetail() {
// 	var row=$("#table4").datagrid('getSelections');
//     linkbutton_click('open_dialog',{dialog:'#detDialog4'});
//     $('.schemename').val(row[0].schemename);
//     $('.schemetype').val(row[0].schemetype);
//     $('.checkobject').val(row[0].checkobject);
//     $('.businesspolice').val(row[0].businesspolice);
//     $('.scheduletime').val(row[0].scheduletime);
//
// }
// function spe() {
// 	$("#detDialog4").dialog('close');
// 	$("#table4").datagrid('reload');
// }
// //前台增加方法
// function addSpe() {
// 	$("#speForm").form('submit', {
// 		url: "/table4/addData4/",
// 		onSubmit: function () {
// 			return true
// 		},
// 		success: function (data) {
// 			$("#speDialog").dialog('close');
// 			$("#table4").datagrid('reload');
//
// 		}
// 	});
// }
// //前台删除方法
// function speDel() {
// 	var data = $("#table4").datagrid('getSelections');
// 	if(data.length == 0){
// 		$.messager.alert('警告','请至少选择一条数据','warning');
// 		// return false;
// 	}
// 	else{
// 	$.messager.confirm('确认删除框','是否确定删除选中记录?',function(ok){
// 		if(ok){
// 			var ids = '';
// 			for (var i in data){
// 				ids += data[i].id + ',';
// 			}
// 			ids = ids.substr(0, ids.length -1);
// 			$.get('/table4/delData4/',{data:ids},function(msg){
// 				$("#table4").datagrid('reload');
// 			})
// 		}
// 	})
// 		}
// }
// //前台修改方法
// function changeSpe() {
// 	var row=$("#table4").datagrid('getSelections');
// 	if(row.length==0||row.length>1) {
// 		$.messager.confirm('警告', '请选择一条数据', 'warning');
// 	}
// 		else{
// 		linkbutton_click('open_dialog',{dialog:'#changeSpe'});
// 		$('.schemenamechange').val(row[0].schemename);
// 		$('.schemetypechange').val(row[0].schemetype);
// 		$('.checkobjectchange').val(row[0].checkobject);
//         $('.businesspolicechange').val(row[0].businesspolice);
//         $('.scheduletimechange').val(row[0].scheduletime);
// 		$('.idchange').val(row[0].id);
// 	}
// }
//
// function table4preserved() {
// 	$('#change_list4').form('submit', {
// 		url: "/table4/changeSpe/",
// 		onSubmit: function () {
// 			return true
// 		},
// 		success: function (data) {
// 			$('#changeSpe').dialog('close');
// 			$('#table4').datagrid('reload');
// 		}
// 	});
// }
//
