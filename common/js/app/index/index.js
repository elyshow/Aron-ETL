// $(function(){
// 	$("#mylist").datagrid({
// 		columns:[[
// 			{field:'checkbox',checkbox:true},
// 			{field:'student_name',title:'姓名',width:'40%',},
// 			{field:'age',title:'年龄',width:'30%',},
// 			{field:'sex',title:'性别',width:'20%',},
// 			{field:'oper',title:'操作',width:'10%',formatter:func},
// 		]]
// 	})
//
// 	$("#combo_list").combobox({
// 		textField:'bbb',
// 		valueField:'aaa',
// 		data:[{
// 			"value":1,
// 			"text":"text1"
// 		},{
// 			"id":2,
// 			"text":"text2"
// 		},{
// 			"id":3,
// 			"text":"text3",
// 			"selected":true
// 		},{
// 			"id":4,
// 			"text":"text4"
// 		},{
// 			"id":5,
// 			"text":"text5"
// 		}],
// 		onChange:function(newValue,oldValue){
//
// 		},
// 		onSelect:function(record){
// 			console.log(record)
// 		}
// 	}).combobox('select','5').combobox('disabled');
// })
//
//
// function func(v,r,i){
// 	return  '<a class="easyui-linkbutton" href="javascript:;" data-options="iconCls:\'icon-edit\'">编辑</a>' +
// 			'<a class="easyui-linkbutton" href="javascript:;" data-options="iconCls:\'icon-cancel\'">删除</a>'
// }
//
//
//
//
// def dataList(request):
// 	datalist = Student.objects.all()
// 	list = []
//
// 	for i in dataList:
// 		temp = {
// 			'student_name':dataList[i].pname,
// 			'age':dataList[i].pname,
// 			'sex':dataList[i].pname,
// 		}
// 		list.append(temp)
//
// 	return HtttpResponse(json.dumps(list), 'application/json')