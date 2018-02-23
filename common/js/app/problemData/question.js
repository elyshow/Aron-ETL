$(function(){
	$("#mylist").datagrid({
		url: "/huafeng/question_table/",
		method:'post',
		toolbar:'#toolbar',
		// onClickRow:function(row){
		// 	domDetail()
		// },
		// onDblClickRow:function(row){
		// 	domDetail()
		// },
		columns:[[
            {field:'checkbox',checkbox:true},
			{field:'schemename',title:'方案名称',width:'26%',align:'center'},
			{field:'checkobject',title:'校验字段',width:'25%',align:'center'},
			// {field:'problemtable',title:'问题记录表',width:'20%',align:'center'},
			{field:'problemrecords',title:'问题记录数',width:'25%',align:'center'},
			{field:'repairrecords',title:'已修复记录数',width:'25%',align:'center'},
        ]],
	})
	$('#search').searchbox({
        prompt:'请输入方案名称',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#mylist').datagrid('load', {condition:v})
        }
    })
})

function domDetail() {
	var data = $("#mylist").datagrid('getSelected');
	data_scheme_name=data.schemename;
	console.log(data);
	console.log(data_scheme_name);
	$.get('/huafeng/wrong_request/',{data:data_scheme_name},function(msg){
		window.open('/huafeng/wrong','_self')
		$("#mylist").datagrid('unselectAll')
	})
}