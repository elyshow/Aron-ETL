$(function(){
	$("#mylist3").datagrid({
		url: "/huafeng/report_table/",
		method:'post',
		toolbar:'#toolbar',
		onClickRow:function(row){
			domDetail()
		},
		onDblClickRow:function(row){
			domDetail()
		},
		columns:[[
		    {field:'id',title:'序号',width:'5%',align:'left'},
			{field:'scheme_name',title:'报告名称',width:'25%',align:'left'},
			{field:'scheme_type',title:'方案类型',width:'15%',align:'left'},
			{field:'check_object',title:'报告时间',width:'20%',align:'left'},
			{field:'problem_records',title:'浏览数据量',width:'8%',align:'left'},
			{field:'repair_records',title:'发现问题数',width:'8%',align:'left'},
        ]],
	})
	$('#search').searchbox({
        prompt:'请输入方案名称',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#mylist3').datagrid('load', {condition:v})
        }
    })
})

function domDetail() {
	var data = $("#mylist3").datagrid('getSelected');
	data_scheme_name=data.schemename;
	console.log(data);
	console.log(data_scheme_name);
	$.get('/huafeng/journal_request/',{data:data_scheme_name},function(msg){
		window.open('/huafeng/journal','_self')
		$("#mylist3").datagrid('unselectAll')
	})
}