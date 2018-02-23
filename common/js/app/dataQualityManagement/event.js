/**
 *
 */
// /*第二个选项卡*/
//
//            columns:[[
//             {field:'checkbox',checkbox:true},
//             {field:'rule_name',title:'规则名称',width:'20%',align:'center'},
//             {field:'object',title:'对象类词',width:'15%',align:'center'},
//             {field:'identifier',title:'标识符',width:'10%',align:'center'},
//             {field:'chinese_name',title:'中文名称',width:'15%',align:'center'},
//             {field:'data_type',title:'数据类型',width:'10%',align:'center'},
//             {field:'operate',title:'操作',width:'25%',align:'center',formatter: operate},
//         ]],
//   
//    
// /*第3个选项卡*/
// $(function(){
//        $("#table3").datagrid({
//             url:'/table3/showData3/',
//             autoRowHeight:true,
//             columns:[[
//             {field:'checkbox',checkbox:true},
//             {field:'scheme_name',title:'方案名称',width:'20%',align:'center'},
//             {field:'check_object',title:'校验对象',width:'15%',align:'center'},
//             {field:'business_classification',title:'业务分类',width:'10%',align:'center'},
//             {field:'schedule_time',title:'调度时间',width:'15%',align:'center'},
//             {field:'whether_publish',title:'是否发布',width:'10%',align:'center'},
//             {field:'operate',title:'操作',width:'25%',align:'center',formatter: operate},
//         ]], onLoadSuccess:function(){
//              // 图标
//             $('.search').linkbutton({
//                iconCls: 'icon-search',
//             });
//             $('.editor').linkbutton({
//                iconCls: 'icon-edit'
//             });
//             $('.delete').linkbutton({
//                iconCls: 'icon-cancel'
//             });
//     },
//        })
// function operate(v,r,i){
//             var r = $('#table1').datagrid('getSelected');
//             if (r){
//                 $('#mydialog').dialog('close');
//                 r.id = null;
//                 $('#mydialog').dialog('open');
//             }
//             if (r){
//                 $('#mydialog1').dialog('close');
//                 r.id = null;
//                 $('#mydialog1').dialog('open');
//             }
// 	return  '<a class="editor" href="javascript:ediData2();" style="margin:5px 5px; " data-options=" ">修改</a>'+'&nbsp;'+
//             '<a class="delete" href="javascript:(delData2());" data-options="">删除</a>'
// }
//
//
// })
// function ediData3() {
// 	var row=$("#table3").datagrid('getSelections');
//     console
//     linkbutton_click('open_dialog',{dialog:'#mydialog2'});
//     $('.rule_name').val(row[0].rule_name);
//     $('.object').val(row[0].object);
//     $('.identifier').val(row[0].identifier);
//     $('.chinese_name').val(row[0].chinese_name);
//     $('.data_type').val(row[0].data_type);
//
// }
// function delData3() {
// 	var data = $("#table3").datagrid('getSelections');
// 	if(data.length == 0){
// 		$.messager.alert('警告','请至少选择一条数据','warning');
// 		// return false;
// 	}
// 	else{
// 	$.messager.confirm('确认删除框','是否确定删除选中记录?',function(ok){
// 		if(ok){
// 			var ids = '';
// 			for (var i in data){
// 				ids += data[i].rule_name + ',';
// 			}
// 			ids = ids.substr(0, ids.length -1);
// 			$.get('/table3/delData/',{data:ids},function(msg){
// 				$("#table3").datagrid('reload');
// 			})
// 		}
// 	})
// 		}
// }
//
//
//
//
// /*第4个选项卡*/
// $(function(){
//        $("#table4").datagrid({
//             url:'/table4/showData4/',
//             autoRowHeight:true,
//             columns:[[
//             {field:'checkbox',checkbox:true},
//             {field:'scheme_name',title:'方案名称',width:'20%',align:'center'},
//             {field:'scheme_type',title:'方案类型',width:'15%',align:'center'},
//             {field:'check_object',title:'校验对象',width:'10%',align:'center'},
//             {field:'business_police',title:'业务警种',width:'10%',align:'center'},
//             {field:'schedule_time',title:'调度时间',width:'15%',align:'center'},
//             {field:'operate',title:'操作',width:'25%',align:'center',formatter: operate},
//         ]],onLoadSuccess:function(){
//              // 图标
//             $('.search').linkbutton({
//                iconCls: 'icon-search',
//             });
//             $('.editor').linkbutton({
//                iconCls: 'icon-edit'
//             });
//             $('.delete').linkbutton({
//                iconCls: 'icon-cancel'
//             });
//     },
//        })
// function operate(v,r,i){
//             var r = $('#table4').datagrid('getSelected');
//             if (r){
//                 $('#mydialog').dialog('close');
//                 r.id = null;
//                 $('#mydialog').dialog('open');
//             }
//             if (r){
//                 $('#mydialog1').dialog('close');
//                 r.id = null;
//                 $('#mydialog1').dialog('open');
//             }
// 	return  '<a class="editor" href="javascript:ediData4();" style="margin:5px 5px; " data-options=" ">修改</a>'+'&nbsp;'+
//             '<a class="delete" href="javascript:(delData4());" data-options="">删除</a>'
// }
//
//
// })
// function ediData4() {
// 	var row=$("#table4").datagrid('getSelections');
//     linkbutton_click('open_dialog',{dialog:'#mydialog2'});
//     $('.rule_name').val(row[0].rule_name);
//     $('.object').val(row[0].object);
//     $('.identifier').val(row[0].identifier);
//     $('.chinese_name').val(row[0].chinese_name);
//     $('.data_type').val(row[0].data_type);
//
// }
// function delData4() {
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
// 				ids += data[i].rule_name + ',';
// 			}
// 			ids = ids.substr(0, ids.length -1);
// 			$.get('/table4/delData/',{data:ids},function(msg){
// 				$("#table4").datagrid('reload');
// 			})
// 		}
// 	})
// 		}
// }
//
// /*第5个选项卡*/
// $(function(){
//        $("#table5").datagrid({
//           url:'/table5/showData5/',
//            autoRowHeight:true,
//         columns:[[
//             {field:'checkbox',checkbox:true},
//             {field:'scheme_name',title:'方案名称',width:'15%',align:'center'},
//             {field:'scheme_type',title:'方案类型',width:'15%',align:'center'},
//             {field:'schedule_plan',title:'调度计划',width:'15%',align:'center'},
//             {field:'last_execution_status',title:'上次执行状态',width:'10%',align:'center'},
//             {field:'last_execution_time',title:'上次执行时间',width:'15%',align:'center'},
//             {field:'current_status',title:'当前状态',width:'5%',align:'center'},
//             {field:'operate',title:'操作',width:'15%',align:'center',formatter: operate},
//         ]],onLoadSuccess:function(){
//              // 图标
//             $('.search').linkbutton({
//                iconCls: 'icon-search',
//             });
//             $('.editor').linkbutton({
//                iconCls: 'icon-edit'
//             });
//             $('.delete').linkbutton({
//                iconCls: 'icon-cancel'
//             });
//     },
//        })
// function operate(v,r,i){
//             var r = $('#table4').datagrid('getSelected');
//             if (r){
//                 $('#mydialog').dialog('close');
//                 r.id = null;
//                 $('#mydialog').dialog('open');
//             }
//             if (r){
//                 $('#mydialog1').dialog('close');
//                 r.id = null;
//                 $('#mydialog1').dialog('open');
//             }
// 	return  '<a class="editor" href="javascript:ediData4();" style="margin:5px 5px; " data-options=" ">修改</a>'+'&nbsp;'+
//             '<a class="delete" href="javascript:(delData4());" data-options="">删除</a>'
// }
//
//
// })
// function ediData5() {
// 	var row=$("#table5").datagrid('getSelections');
//     console
//     linkbutton_click('open_dialog',{dialog:'#mydialog2'});
//     $('.rule_name').val(row[0].rule_name);
//     $('.object').val(row[0].object);
//     $('.identifier').val(row[0].identifier);
//     $('.chinese_name').val(row[0].chinese_name);
//     $('.data_type').val(row[0].data_type);
//
// }
// function delData5() {
// 	var data = $("#table5").datagrid('getSelections');
// 	if(data.length == 0){
// 		$.messager.alert('警告','请至少选择一条数据','warning');
// 		// return false;
// 	}
// 	else{
// 	$.messager.confirm('确认删除框','是否确定删除选中记录?',function(ok){
// 		if(ok){
// 			var ids = '';
// 			for (var i in data){
// 				ids += data[i].rule_name + ',';
// 			}
// 			ids = ids.substr(0, ids.length -1);
// 			$.get('/table5/delData/',{data:ids},function(msg){
// 				$("#table5").datagrid('reload');
// 			})
// 		}
// 	})
// 		}
// }
//
//
// /*第6个选项卡*/
// $(function(){
//        $("#table6").datagrid({
//           url:'/table6/showData6/',
//             autoRowHeight:true,
//         columns:[[
//             {field:'checkbox',checkbox:true},
//             {field:'scheme_name',title:'方案名称',width:'18%',align:'center'},
//             {field:'start_time',title:'开始时间',width:'15%',align:'center'},
//             {field:'consuming_time',title:'耗时（S)',width:'5%',align:'center'},
//             {field:'check_records',title:'校验记录数',width:'8%',align:'center'},
//             {field:'new_records',title:'新增记录数',width:'8%',align:'center'},
//             {field:'found_problem_records',title:'发现问题记录数',width:'10%',align:'center'},
//             {field:'new_problem_records',title:'新增问题记录数',width:'10%',align:'center'},
//             {field:'abnormal_log',title:'异常日志',width:'15%',align:'center',formatter: operate},
//         ]],onLoadSuccess:function(){
//              // 图标
//             $('.search').linkbutton({
//                iconCls: 'icon-search',
//             });
//             $('.editor').linkbutton({
//                iconCls: 'icon-edit'
//             });
//             $('.delete').linkbutton({
//                iconCls: 'icon-cancel'
//             });
//     },
//        })
// function operate(v,r,i){
//             var r = $('#table4').datagrid('getSelected');
//             if (r){
//                 $('#mydialog').dialog('close');
//                 r.id = null;
//                 $('#mydialog').dialog('open');
//             }
//             if (r){
//                 $('#mydialog1').dialog('close');
//                 r.id = null;
//                 $('#mydialog1').dialog('open');
//             }
// 	return  '<a class="editor" href="javascript:ediData4();" style="margin:5px 5px; " data-options=" ">修改</a>'+'&nbsp;'+
//             '<a class="delete" href="javascript:(delData4());" data-options="">删除</a>'
// }
//
//
// })
// function ediData6() {
// 	var row=$("#table6").datagrid('getSelections');
//     console
//     linkbutton_click('open_dialog',{dialog:'#mydialog2'});
//     $('.rule_name').val(row[0].rule_name);
//     $('.object').val(row[0].object);
//     $('.identifier').val(row[0].identifier);
//     $('.chinese_name').val(row[0].chinese_name);
//     $('.data_type').val(row[0].data_type);
//
// }
// function delData6() {
// 	var data = $("#table6").datagrid('getSelections');
// 	if(data.length == 0){
// 		$.messager.alert('警告','请至少选择一条数据','warning');
// 		// return false;
// 	}
// 	else{
// 	$.messager.confirm('确认删除框','是否确定删除选中记录?',function(ok){
// 		if(ok){
// 			var ids = '';
// 			for (var i in data){
// 				ids += data[i].rule_name + ',';
// 			}
// 			ids = ids.substr(0, ids.length -1);
// 			$.get('/table6/delData/',{data:ids},function(msg){
// 				$("#table6").datagrid('reload');
// 			})
// 		}
// 	})
// 		}
// }
//
//
//
//
//
//
//
//
//
//





