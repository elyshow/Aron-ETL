$(function(){
	$("#codeList").datagrid({
		url:'/standardIndex/codeStandardIndex/codeStandard/',
		rownumbers:'true',
		columns:[[
			{field:'checkbox',checkbox:true},
			{field:'codename',title:'代码名称',width:'14%',},
			{field:'standardnum',title:'标准编号',width:'15%',},
			{field:'codetable',title:'代码表',width:'15%',},
			{field:'datasource',title:'数据源',width:'15%',},
			{field:'registertime',title:'注册时间',width:'15%',},
			{field:'oper',title:'操作',width:'10%',formatter:func},
		]]
	})
	 $('#codeSearchBox').searchbox({
        prompt:'请输入代码表搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#codeList').datagrid('load', {condition:v,type:1});
			console.log(v);
			console.log('111');
        }
    })
})


function func(v,r,i){
	return  '<a class="easyui-linkbutton" href="javascript:;" data-options="iconCls:\'icon-edit\'">编辑</a>' +
			'<a class="easyui-linkbutton" href="javascript:;" data-options="iconCls:\'icon-cancel\'">删除</a>'
}
