$(function(){
	$("#mylist").datagrid({
		url: "/huafeng/interfacetable_index/",
		method:'post',
		singleSelect:true,
		toolbar:'#toolbar',
		columns:[[
		    {field:'idAPI',title:'接口编号',width:'24%',align:'left'},
            {field:'field_chinese',title:'接口返回字段中文名',width:'25%',align:'left'},
			{field:'field_english',title:'接口返回字段英文名',width:'25%',align:'left'},
            {field:'show_type',title:'接口返回字段类型',width:'25%',align:'left'},
        ]],
	})
})

