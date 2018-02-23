/**
 * Created by Administrator on 2016-08-18.
 */
// //增加
// function adddataway(){
//     var rowsData1 = $('#drag4').datagrid('getRows');
//     console.log(rowsData1)
//     var json1 =JSON.stringify(rowsData1);
//     console.log(json1)
//     var rowsData2 = $('#mylist_condition').datagrid('getRows');
//     console.log(rowsData2)
//     var json2 =JSON.stringify(rowsData2);
//     console.log(json2)
//     $().linkbutton('saveChange', {
//     form:'#datawayForm',
//     dialog:'#metDialog',
//     url:'/dataway/saveData/',
//     param:{
//         hierarchy1: json1,
//         hierarchy2: json2,
//     },
//     })
// }

//前台取值
$('#save4').linkbutton({
		onClick:function () {
			var form1 = $("#basic_info").serialize();
			var form2 = $("#infoFile").serialize();
			var form3 = $("#rules").datagrid('getRows');
			var form4 = $("#fields").datagrid('getRows');
			var form5 = $("#schedum").serialize();
			console.log(form1)
			console.log(form2)
			console.log(form3)
			console.log(form4)
			console.log(form5)

//给后台传值
// 			$('#cleaningForm').form('submit',{
// 				url:'/tab/list3/',
// 				onSubmit:function(param){
//
//                         param.form1 = getPostDataFromTable('basic_info', 'datasource', 'keyword');
//                         param.form2 = getPostDataFromTable('infoFile', 'schemename', 'fieldname','inputperson','checkfun','detail');
//                         param.form3 = getPostDataFromTable('rules', 'ruletype', 'methodname','fieldname','rulename','serious');
// 						param.form4 = getPostDataFromTable('fields', 'fieldname');
//                         param.form5 = getPostDataFromTable('schedum', 'fromFieldName', 'ruleID');
//
// 				},
// 				success:function (res) {
// 					$('.form_reset').form('reset');
// 					$("#basDialog").dialog('close');
// 					$('#table3').datagrid('reload');
//
// 				}
// 			})
//
 		}
	})
//
// function getPostDataFromTable(tableId, firstField, secondField){
//     var tableRows = $('#'+tableId).datagrid('getData').rows;
//     var dataObj = new Object();
//     for(var i in tableRows){
//         dataObj[tableRows[i][firstField]] = tableRows[i][secondField];
//     }
//     return JSON.stringify(dataObj);
// }
//
