(window.webpackJsonp=window.webpackJsonp||[]).push([[17,18],{650:function(e,t,n){var content=n(678);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(81).default)("4ee98e4a",content,!0,{sourceMap:!1})},663:function(e,t,n){"use strict";n.r(t);n(70),n(83),n(370);var o={model:{prop:"areChecked",event:"change"},props:["areChecked","value","id","disabled","label","allowMultiple"],data:function(){return{checked:this.value||!1}},computed:{classes:function(){return{active:Array.isArray(this.areChecked)?this.areChecked.includes(this.value):this.checked,disabled:this.disabled}}},watch:{value:function(){this.checked=!!this.value}},methods:{toggleCheck:function(){if(!this.disabled){var e=this.areChecked,t=e.indexOf(this.value);t>=0?e.splice(t,1):(e.length&&!this.allowMultiple&&(e=[]),e.push(this.value)),this.$emit("change",e)}}}},r=(n(677),n(42)),component=Object(r.a)(o,(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"re-annotation-button",class:[e.classes,e.allowMultiple?"multiple":"single"]},[n("label",{staticClass:"button",attrs:{for:e.id},on:{click:function(t){return t.preventDefault(),e.toggleCheck.apply(null,arguments)}}},[n("span",{staticClass:"annotation-button-data__text",attrs:{title:e.label.class}},[e._v(e._s(e.label.class)+"\n    ")]),e._v(" "),e.label.score>0?n("div",{staticClass:"annotation-button-data__info"},[n("span",[e._v(e._s(e._f("percent")(e.label.score)))])]):e._e()]),e._v(" "),n("div",{staticClass:"annotation-button-container",attrs:{tabindex:"0"},on:{click:function(t){return t.stopPropagation(),e.toggleCheck.apply(null,arguments)}}},[n("input",{attrs:{id:e.id,type:"checkbox",disabled:e.disabled},domProps:{value:e.value,checked:e.checked}})])])}),[],!1,null,"b966c16e",null);t.default=component.exports},677:function(e,t,n){"use strict";n(650)},678:function(e,t,n){var o=n(80)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.re-annotation-button[data-v-b966c16e]{width:auto;margin:16px 8px 16px 0;display:inline-flex;position:relative}.re-annotation-button .annotation-button-container[data-v-b966c16e]{display:none}.re-annotation-button.label-button[data-v-b966c16e]{margin:3.5px;color:#353664;padding:0;transition:all .3s ease;max-width:238px}.re-annotation-button.label-button .button[data-v-b966c16e]{outline:none;cursor:pointer;background:#f0f0fe;border-radius:8px;height:40px;line-height:40px;padding-left:.5em;padding-right:.5em;width:100%;display:flex;font-family:"Outfit","Helvetica","Arial",sans-serif;font-weight:500;overflow:hidden;color:#353664;box-shadow:0;transition:all .2s ease-in-out}.re-annotation-button.label-button.predicted-label .button[data-v-b966c16e]{background:#d6d6ff}.re-annotation-button.label-button.active[data-v-b966c16e]{transition:all .2s ease-in-out;box-shadow:none}.re-annotation-button.label-button.active .button[data-v-b966c16e]{transition:all .2s ease-in-out;background:#4c4ea3;box-shadow:none}.re-annotation-button.label-button.active:hover .button[data-v-b966c16e]{transition:all .2s ease-in-out;box-shadow:0 0 1px 0 hsla(0,0%,83.1%,.5),inset 0 -2px 6px 0 #3b3c81}.re-annotation-button.label-button.active[data-v-b966c16e]:after{display:none!important}.re-annotation-button.label-button.active .annotation-button-data__info[data-v-b966c16e],.re-annotation-button.label-button.active .annotation-button-data__score[data-v-b966c16e],.re-annotation-button.label-button.active .annotation-button-data__text[data-v-b966c16e]{color:#fff}.re-annotation-button.label-button .annotation-button-data[data-v-b966c16e]{overflow:hidden;transition:transform .3s ease}.re-annotation-button.label-button .annotation-button-data__text[data-v-b966c16e]{max-width:200px;overflow:hidden;text-overflow:ellipsis;display:inline-block;white-space:nowrap;vertical-align:top}.re-annotation-button.label-button .annotation-button-data__info[data-v-b966c16e]{margin-right:0;margin-left:1em;transform:translateY(0);transition:all .3s ease}.re-annotation-button.label-button .annotation-button-data__score[data-v-b966c16e]{min-width:40px;font-size:12px;font-size:.75rem;display:inline-block;text-align:center;line-height:1.5em;border-radius:2px}.re-annotation-button.label-button:not(.active):hover .button[data-v-b966c16e]{box-shadow:0 0 1px 0 hsla(0,0%,83.1%,.5),inset 0 -2px 6px 1px #bbbce0}.re-annotation-button.disabled[data-v-b966c16e]{opacity:.5}.re-annotation-button.non-reactive[data-v-b966c16e]{pointer-events:none;cursor:pointer}.re-annotation-button.non-reactive .button[data-v-b966c16e]{background:#fff!important;color:#fff;border:1px solid #f2f3f7}.re-annotation-button[data-v-b966c16e]:not(.disabled),.re-annotation-button:not(.disabled) .annotation-button[data-v-b966c16e]{cursor:pointer}.re-annotation-button .annotation-button[data-v-b966c16e]{height:20px;padding-left:8px;line-height:20px}',""]),e.exports=o},696:function(e,t,n){n(153).register({ignore:{width:17,height:18,viewBox:"0 0 17 18",data:'<defs><path pid="0" id="svgicon_ignore_a" d="M0 0h16.914v17.826H0z"/></defs><g _fill="none" fill-rule="evenodd"><path pid="1" d="M14.81 3.525l2.018-2.161L15.365 0l-2.076 2.224A7.937 7.937 0 008.914.913c-4.411 0-8 3.589-8 8a7.94 7.94 0 001.632 4.822L0 16.462l1.463 1.364 2.479-2.657a7.953 7.953 0 004.972 1.744c4.411 0 8-3.59 8-8a7.961 7.961 0 00-2.104-5.388M2.914 8.913c0-3.31 2.691-6 6-6 1.087 0 2.104.295 2.984.802L3.931 12.25a5.963 5.963 0 01-1.017-3.338m6 6A5.962 5.962 0 015.313 13.7l8.13-8.711a5.966 5.966 0 011.471 3.923c0 3.309-2.691 6-6 6" _fill="#000"/></g>'}})},709:function(e,t,n){var content=n(792);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(81).default)("9d0a067a",content,!0,{sourceMap:!1})},791:function(e,t,n){"use strict";n(709)},792:function(e,t,n){var o=n(80)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.label-button[data-v-b9e03d42]{min-width:80px;max-width:238px}.annotation-area[data-v-b9e03d42]{margin-top:2em}.feedback-interactions[data-v-b9e03d42]{margin:0 auto;padding-right:0}@media (min-width:1451px){.feedback-interactions[data-v-b9e03d42]:not(.fixed){max-width:calc(60% + 200px);margin-left:0}}.list__item--annotation-mode .feedback-interactions[data-v-b9e03d42]{padding-right:200px}.feedback-interactions__more[data-v-b9e03d42]{align-self:center;margin:3.5px;text-decoration:none;font-weight:500;font-family:"Outfit","Helvetica","Arial",sans-serif;outline:none;padding:.5em;border-radius:5px;transition:all .2s ease-in-out;display:inline-block}.feedback-interactions__more[data-v-b9e03d42]:hover{transition:all .2s ease-in-out;background:#f5f5f5}.label-button.fixed[data-v-b9e03d42]{width:24%}.label-button.fixed[data-v-b9e03d42]  .annotation-button-data__info{margin-right:0!important;margin-left:auto!important}',""]),e.exports=o},817:function(e,t,n){"use strict";n.r(t);n(38),n(33),n(51),n(52);var o=n(36),r=n(17),c=n(63),l=(n(46),n(44),n(43),n(10),n(25),n(371),n(154),n(62),n(32),n(45),n(369),n(696),n(26)),d=n(156);function h(object,e){var t=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(object,e).enumerable}))),t.push.apply(t,n)}return t}function f(e){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?h(Object(source),!0).forEach((function(t){Object(r.a)(e,t,source[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(source)):h(Object(source)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(source,t))}))}return e}var L={mixins:[Object(d.a)({idProp:function(e){return"".concat(e.dataset.name,"-").concat(e.record.id)}})],props:{record:{type:Object,required:!0},dataset:{type:Object,required:!0}},idState:function(){return{searchText:"",selectedLabels:[],shownLabels:l.a.MAX_VISIBLE_LABELS}},watch:{annotationLabels:function(e,t){e!==t&&(this.selectedLabels=this.appliedLabels)}},computed:{searchText:{get:function(){return this.idState.searchText},set:function(e){this.idState.searchText=e}},selectedLabels:{get:function(){return this.idState.selectedLabels},set:function(e){this.idState.selectedLabels=e}},shownLabels:{get:function(){return this.idState.shownLabels},set:function(e){this.idState.shownLabels=e}},maxVisibleLabels:function(){return l.a.MAX_VISIBLE_LABELS},isMultiLabel:function(){return this.dataset.isMultiLabel},labels:function(){var e=Object.assign.apply(Object,[{}].concat(Object(c.a)(this.dataset.labels.map((function(label){return Object(r.a)({},label,{score:0,selected:!1})})))));return this.annotationLabels.forEach((function(label){e[label.class]={score:0,selected:!0}})),this.predictionLabels.forEach((function(label){var t=e[label.class]||label;e[label.class]=f(f({},t),{},{score:label.score})})),Object.entries(e).map((function(e){var t=Object(o.a)(e,2);return f({class:t[0]},t[1])}))},sortedLabels:function(){return this.labels.slice().sort((function(a,b){return a.score>b.score?-1:1}))},filteredLabels:function(){var e=this;return this.sortedLabels.filter((function(label){return label.class.toLowerCase().match(e.searchText.toLowerCase())}))},visibleLabels:function(){var e=this.filteredLabels.filter((function(e){return e.selected})).length,t=this.shownLabels<this.filteredLabels.length?this.shownLabels-e:this.shownLabels,n=0;return this.filteredLabels.filter((function(e){return e.selected?e:n<t?(n++,e):void 0}))},annotationLabels:function(){return this.record.annotation?this.record.annotation.labels:[]},predictionLabels:function(){return this.record.prediction?this.record.prediction.labels:[]},appliedLabels:function(){return this.filteredLabels.filter((function(e){return e.selected})).map((function(label){return label.class}))},predictedAs:function(){return this.record.predicted_as},UXtest:function(){return this.$route.query.UXtest}},mounted:function(){this.selectedLabels=this.appliedLabels},methods:{updateLabels:function(e){this.isMultiLabel||e.length>0?this.annotate():this.resetAnnotations()},resetAnnotations:function(){this.$emit("reset",this.record)},annotate:function(){this.$emit("validate",{labels:this.selectedLabels})},expandLabels:function(){this.shownLabels=this.filteredLabels.length},collapseLabels:function(){this.shownLabels=this.maxVisibleLabels},onSearchLabel:function(e){this.searchText=e}}},m=(n(791),n(42)),component=Object(m.a)(L,(function(){var e=this,t=e.$createElement,n=e._self._c||t;return e.labels.length?n("div",{staticClass:"annotation-area"},[e.labels.length>e.maxVisibleLabels?n("label-search",{attrs:{searchText:e.searchText},on:{input:e.onSearchLabel}}):e._e(),e._v(" "),n("div",{class:["fixed"===e.UXtest?"fixed":null,"feedback-interactions"]},[e._l(e.visibleLabels,(function(label){return n("ClassifierAnnotationButton",{key:""+label.class,class:["label-button",e.predictedAs.includes(label.class)?"predicted-label":null,"fixed"===e.UXtest?"fixed":null],attrs:{id:label.class,"allow-multiple":e.isMultiLabel,label:label,"data-title":label.class,value:label.class},on:{change:e.updateLabels},model:{value:e.selectedLabels,callback:function(t){e.selectedLabels=t},expression:"selectedLabels"}})})),e._v(" "),e.visibleLabels.length<e.filteredLabels.length?n("a",{staticClass:"feedback-interactions__more",attrs:{href:"#"},on:{click:function(t){return t.preventDefault(),e.expandLabels()}}},[e._v("+"+e._s(e.filteredLabels.length-e.visibleLabels.length))]):e.visibleLabels.length>e.maxVisibleLabels?n("a",{staticClass:"feedback-interactions__more",attrs:{href:"#"},on:{click:function(t){return t.preventDefault(),e.collapseLabels()}}},[e._v("Show less")]):e._e()],2)],1):e._e()}),[],!1,null,"b9e03d42",null);t.default=component.exports;installComponents(component,{LabelSearch:n(714).default,ClassifierAnnotationButton:n(663).default})}}]);