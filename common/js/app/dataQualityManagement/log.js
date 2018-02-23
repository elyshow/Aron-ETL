/**
 * Created by Administrator on 2016-08-13.
 */
/**
 * Created by Administrator on 2016-08-12.
 */
/*第六个选项卡*/
$(function(){
	$("#table6").datagrid({
		url:'',
		toolbar:'#logToolBar',
		method:'post',
         autoRowHeight:true,
		columns:[[
			{field:'checkbox',checkbox:true},
            {field:'schemename',title:'方案名称',width:'18%',align:'center'},
			{field:'card',title:'校验字段',width:'20%',align:'center'},
			{field:'starttime',title:'开始时间',width:'20%',align:'center'},
            {field:'checkrecords',title:'校验记录数',width:'20%',align:'center'},
            {field:'newrecords',title:'成功记录数',width:'20%',align:'center'},
            {field:'foundproblemrecords',title:'发现问题记录数',width:'13%',align:'center'},
			{field:'oper',title:'操作',align:'center',width:'20%'},
		]],  onLoadSuccess:function(){
             // 图标
            $('.detail').linkbutton({
               iconCls: 'icon-search',
            });

    },
	})
     $("#combobox_type6").combobox({
        width:155,
        valueField:'id',
        textField:"text",
        data:[{
            "id": "全部",
            "text": "全部"
        }, {
            "id": "常住人口信息基础方案",
            "text": "常住人口信息基础方案"
        }, {
            "id":"其他",
            "text":"其他"
        }
        ],
    })

	 $('#logSearchBox').searchbox({
        prompt:'请输入搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#table6').datagrid('load', {condition:v,type:1});
			// console.log(v);
			// console.log('111');
        }
    })

})

//前台删除方法
function logDel() {
	var data = $("#log").datagrid('getSelections');
	if(data.length == 0){
		$.messager.alert('警告','请至少选择一条数据','warning');
		// return false;
	}
	else{
	$.messager.confirm('确认删除框','是否确定删除选中记录?',function(ok){
		if(ok){
			var ids = '';
			for (var i in data){
				ids += data[i].id + ',';
			}
			ids = ids.substr(0, ids.length -1);
			$.get('/table6/delData6/',{data:ids},function(msg){
				$("#log").datagrid('reload');
			})
		}
	})
		}
}

function Table6Del() {
	var data = $("#table6").datagrid('getSelections');
	if(data.length == 0){
		$.messager.alert('警告','请至少选择一条数据','warning');
		// return false;
	}
	else{
	$.messager.confirm('确认删除框','是否确定删除选中记录?',function(ok){
		if(ok){
			var ids = '';
			for (var i in data){
				ids += data[i].id + ',';
			}
			ids = ids.substr(0, ids.length -1);
			$.get('/table6/deData6/',{data:ids},function(msg){
				$("#table6").datagrid('reload');
			})
		}
	})
		}
}


//查看监测日志
function rezhi() {
	console.log(111)
	window.open('/logList/','_blank');

}


$(function() {
	$("#log").datagrid({
		url: '/logList/loadList6/',
		toolbar: '#logToolBar2',
		method: 'post',
		autoRowHeight: true,
		columns: [[
			{field: 'checkbox', checkbox: true},
			{field: 'id', title: '序号', width: '18%', align: 'center'},
			{field: 'schemename', title: '方案名称', width: '20%', align: 'center'},
			{field: 'card', title: '校验字段', width: '20%', align: 'center'},
			{field: 'starttime', title: '开始时间', width: '20%', align: 'center'},
			{field: 'endtime', title: '结束时间', width: '20%', align: 'center'},
			{field: 'state', title: '状态', width: '13%', align: 'center'},
			{field: 'oper', title: '操作', align: 'center', width: '20%'},
		]],
	})
	 $('#logSearchBox2').searchbox({
        prompt:'请输入搜索',
        height:24,
        width:200,
        searcher:function(v,n){
           $('#table6').datagrid('load', {condition:v,type:1});
			// console.log(v);
			// console.log('111');
        }
    })
})