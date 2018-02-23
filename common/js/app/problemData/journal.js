$(function(){
	$("#mylist4").datagrid({
		url: "/huafeng/journal_table/",
		method:'post',
		toolbar:'#toolbar',
		columns:[[
            {field:'id',title:'序号',width:'20%',align:'center'},
            {field:'schoolname',title:'资源名',width:'20%',align:'center'},
            {field:'provideunit',title:'资源中文名',width:'20%',align:'center'},
            {field:'datasource',title:'数据源',width:'19%',align:'center'},
            {field:'updatetime',title:'评估时间',width:'20%',align:'center'},
      
        ]],
	})
	$('#search').searchbox({
        prompt:'请输入资源名称',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#mylist4').datagrid('load', {condition:v})
        }
    })
})

