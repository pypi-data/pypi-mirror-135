(this.webpackJsonpstreamlit_component_template=this.webpackJsonpstreamlit_component_template||[]).push([[0],{17:function(e,t,n){e.exports={poButton:"style_poButton__3x8Ka"}},18:function(e,t,n){e.exports=n(26)},26:function(e,t,n){"use strict";n.r(t);var o=n(8),a=n.n(o),r=n(15),i=n.n(r),s=n(6),c=n(0),l=n(1),u=n(2),p=n(3),d=n(13),m=n(17),f=n.n(m),g=function(e){Object(u.a)(n,e);var t=Object(p.a)(n);function n(){var e;Object(l.a)(this,n);for(var o=arguments.length,r=new Array(o),i=0;i<o;i++)r[i]=arguments[i];return(e=t.call.apply(t,[this].concat(r))).state={action:"",data:"",uniqueId:"",options:{layer:"",units:""},isFocused:!1},e.render=function(){var t={BakeGeometry:"Bake Geometry",ClearGeometry:"Clear Geometry",DrawGeometry:"Draw Geometry",DisableDraw:"Disable Draw",BakePollinationModel:"Bake Pollination Model"};return a.a.createElement("span",null,e.props.args.action in t&&a.a.createElement("button",{className:f.a.poButton,onClick:e.onClicked,disabled:e.props.disabled,onFocus:e._onFocus,onBlur:e._onBlur},a.a.createElement("span",null,a.a.createElement("img",{style:{margin:"0px 3px 2px 0px"},src:"./img/pollination.png",alt:"logo"})),t[e.props.args.action]))},e.onClicked=function(){if("undefined"!=typeof window.parent.chrome){if("undefined"==typeof window.parent.chrome.webview)return void console.log("[POLLINATION-DEBUG]: webview not found.");var t={action:e.props.args.action,data:e.props.args.data,uniqueId:e.props.args.uniqueId,options:e.props.args.options},n=JSON.stringify(t);window.parent.chrome.webview.postMessage(n),e.setState((function(e){return Object(s.a)(Object(s.a)({},e),{},{action:t.action,data:t.data,uniqueId:t.uniqueId,options:t.options})}),(function(){return d.a.setComponentValue(e.state.action)})),console.log("[POLLINATION-DEBUG]: JSON string sent.")}else console.log("[POLLINATION-DEBUG]: chrome not found.")},e._onFocus=function(){e.setState({isFocused:!0})},e._onBlur=function(){e.setState({isFocused:!1})},e}return Object(c.a)(n)}(d.b),w=Object(d.c)(g);i.a.render(a.a.createElement(a.a.StrictMode,null,a.a.createElement(w,null)),document.getElementById("root"))}},[[18,1,2]]]);
//# sourceMappingURL=main.f34693c1.chunk.js.map