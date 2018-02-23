$(function(){
	$("#mylist").datagrid({
		url: "/huafeng/condition_table/",
		method:'post',
		rownumbers:true,
		singleSelect:true,
		toolbar:'#toolbar',
		columns:[[
		    {field:'id',title:'id',width:'20%',align:'left',hidden:true},      
		    {field:'idAPI',title:'接口编号',width:'25%',align:'left'},
            {field:'field_english',title:'接口查询条件英文名',width:'23%',align:'left'},
			{field:'field_chinese',title:'接口查询条件中文名',width:'23%',align:'left'},
			{field:'show_type',title:'接口查询条件类型',width:'20%',align:'left'},
        ]],
	})
	 $('#mylist').closest('div.datagrid-view').find('div.datagrid-header-rownumber').html('条件顺序')
	 $('#search').searchbox({
        prompt:'请输入接口查询条件',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#mylist').datagrid('load', {condition:v})
        }
    })
})

