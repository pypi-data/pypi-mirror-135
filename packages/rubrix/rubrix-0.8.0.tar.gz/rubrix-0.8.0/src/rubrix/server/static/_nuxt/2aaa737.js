(window.webpackJsonp=window.webpackJsonp||[]).push([[96,37,82,83],{1035:function(e,n,t){"use strict";t(930)},1036:function(e,n,t){var o=t(80)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.sidebar__title[data-v-ae08ce32]{color:#353664;margin-top:.5em;font-size:20px;font-size:1.25rem;font-weight:700}label[data-v-ae08ce32]{display:block;width:calc(100% - 40px);overflow:hidden;text-overflow:ellipsis}.labels[data-v-ae08ce32]{margin-top:3em}.labels strong[data-v-ae08ce32]{margin-bottom:1em;display:block}.info[data-v-ae08ce32]{position:relative;display:flex;margin-bottom:.7em;color:#353664}.scroll[data-v-ae08ce32]{max-height:calc(100vh - 400px);padding-right:1em;margin-right:-1em;overflow:auto}.records-number[data-v-ae08ce32]{margin-right:0;margin-left:auto}',""]),e.exports=o},1068:function(e,n,t){"use strict";t.r(n);t(728),t(154),t(371),t(372);var o={props:{dataset:{type:Object,required:!0}},data:function(){return{selectedOption:{id:"keywords",name:"Keywords"}}},computed:{getKeywords:function(){var e=this.dataset.results.aggregations.words;return Object.fromEntries(Object.entries(e).sort((function(a,b){return b[1]-a[1]})))},options:function(){var e=[];return e.push({id:"keywords",name:"Keywords"}),Object.values(this.dataset.results.aggregations.predicted).length&&e.push({id:"error",name:"Error Distribution"}),e}},methods:{onSelectOption:function(e){this.selectedOption=e}}},r=(t(1035),t(42)),component=Object(r.a)(o,(function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",[t("p",{staticClass:"sidebar__title"},[e._v("Stats")]),e._v(" "),t("StatsSelector",{attrs:{"selected-option":e.selectedOption,options:e.options},on:{selectOption:e.onSelectOption}}),e._v(" "),"error"===e.selectedOption.id?t("StatsErrorDistribution",{attrs:{dataset:e.dataset}}):e._e(),e._v(" "),"keywords"===e.selectedOption.id?[t("div",{staticClass:"scroll"},e._l(e.getKeywords,(function(n,o){return t("div",{key:o},[n>0?t("div",{staticClass:"info"},[t("label",[e._v(e._s(o))]),e._v(" "),t("span",{staticClass:"records-number"},[e._v(e._s(e._f("formatNumber")(n)))])]):e._e()])})),0)]:e._e()],2)}),[],!1,null,"ae08ce32",null);n.default=component.exports;installComponents(component,{StatsSelector:t(743).default,StatsErrorDistribution:t(742).default})},655:function(e,n,t){var content=t(693);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(81).default)("43ffa5aa",content,!0,{sourceMap:!1})},671:function(e,n,t){var content=t(720);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(81).default)("0f0cd61d",content,!0,{sourceMap:!1})},672:function(e,n,t){var content=t(722);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(81).default)("33e06b80",content,!0,{sourceMap:!1})},692:function(e,n,t){"use strict";t(655)},693:function(e,n,t){var o=t(80)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@-webkit-keyframes spin-data-v-7b91666a{to{transform:rotate(.5turn)}}@keyframes spin-data-v-7b91666a{to{transform:rotate(.5turn)}}@-webkit-keyframes bg-data-v-7b91666a{50%{background:#ff541e}}@keyframes bg-data-v-7b91666a{50%{background:#ff541e}}.pie[data-v-7b91666a]{position:relative;width:100px;line-height:100px;border-radius:50%;background:#50cb88;color:transparent;text-align:center;background-image:linear-gradient(90deg,transparent 50%,#ff541e 0)}.pie[data-v-7b91666a],.pie[data-v-7b91666a]:before{transform-origin:left}.pie[data-v-7b91666a]:before{content:"";position:absolute;top:0;left:50%;width:50%;height:100%;border-radius:0 100% 100% 0/50%;background-color:inherit;-webkit-animation:spin-data-v-7b91666a 50s linear infinite,bg-data-v-7b91666a 100s step-end infinite;animation:spin-data-v-7b91666a 50s linear infinite,bg-data-v-7b91666a 100s step-end infinite;-webkit-animation-play-state:paused;animation-play-state:paused;-webkit-animation-delay:inherit;animation-delay:inherit}',""]),e.exports=o},713:function(e,n,t){"use strict";t.r(n);t(368);var o={props:{percent:{type:Number,required:!0}}},r=(t(692),t(42)),component=Object(r.a)(o,(function(){var e=this,n=e.$createElement;return(e._self._c||n)("div",{staticClass:"pie",style:{animationDelay:-e.percent+"s"}},[e._v("\n  "+e._s(e.percent)+"%\n")])}),[],!1,null,"7b91666a",null);n.default=component.exports},719:function(e,n,t){"use strict";t(671)},720:function(e,n,t){var o=t(80)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.pie-chart[data-v-478a0790]{margin:0 auto 2em}.color-bullet[data-v-478a0790]{height:10px;width:10px;border-radius:50%;display:inline-block;margin:.3em .3em .3em 0}.color-bullet.ok[data-v-478a0790]{background:#50cb88}.color-bullet.ko[data-v-478a0790]{background:#ff1e5e}.info[data-v-478a0790]{position:relative;display:flex;margin-bottom:.7em;color:#353664}.info.total[data-v-478a0790]{margin-bottom:1.5em}.records-number[data-v-478a0790]{margin-right:0;margin-left:auto}',""]),e.exports=o},721:function(e,n,t){"use strict";t(672)},722:function(e,n,t){var o=t(80)(!1);o.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.selector[data-v-07fc1970]{position:relative;margin-bottom:2em}.selector__header[data-v-07fc1970]{cursor:pointer;border:1px solid #e9eaed;border-radius:5px;padding:.5em 1em;color:#353664;font-size:13px;font-size:.8125rem;display:flex;align-items:center}.selector__header[data-v-07fc1970]:after{content:"";border-color:#4a4a4a;border-style:solid;border-width:1px 1px 0 0;display:inline-block;height:8px;width:8px;transform:rotate(133deg);transition:all 1.5s ease;margin-bottom:2px;margin-left:auto}.selector__body[data-v-07fc1970]{display:block;padding:1em;background:#fff;border:1px solid #e9eaed;list-style:none;position:absolute;top:100%;z-index:1;width:100%;margin-top:0}.selector__body a[data-v-07fc1970]{padding:.5em 0;display:block;text-decoration:none;outline:none}.selector__body a[data-v-07fc1970]:hover{font-weight:600}',""]),e.exports=o},728:function(e,n,t){var o=t(4),r=t(19),c=t(84);o({target:"Object",stat:!0},{fromEntries:function(e){var n={};return r(e,(function(e,t){c(n,e,t)}),{AS_ENTRIES:!0}),n}})},742:function(e,n,t){"use strict";t.r(n);var o={props:{dataset:{type:Object,required:!0}},computed:{total:function(){return this.dataset.results.total},predicted:function(){return this.dataset.results.aggregations.predicted},KoPercent:function(){return this.predicted.ko/this.total*100}}},r=(t(719),t(42)),component=Object(r.a)(o,(function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",[t("PieChart",{staticClass:"pie-chart",attrs:{percent:e.KoPercent}}),e._v(" "),t("div",{staticClass:"info total"},[t("label",[e._v("Total records")]),e._v(" "),t("span",{staticClass:"records-number"},[e._v("\n      "+e._s(e._f("formatNumber")(e.total))+"\n    ")])]),e._v(" "),t("div",{staticClass:"info"},[t("span",{staticClass:"color-bullet ok"}),e._v(" "),t("label",[e._v("Predicted ok")]),e._v(" "),t("span",{staticClass:"records-number"},[e._v("\n      "+e._s(e._f("formatNumber")(e.predicted.ok))+"\n    ")])]),e._v(" "),t("div",{staticClass:"info"},[t("span",{staticClass:"color-bullet ko"}),e._v(" "),t("label",[e._v("Predicted ko")]),e._v(" "),t("span",{staticClass:"records-number"},[e._v("\n      "+e._s(e._f("formatNumber")(e.predicted.ko))+"\n    ")])])],1)}),[],!1,null,"478a0790",null);n.default=component.exports;installComponents(component,{PieChart:t(713).default})},743:function(e,n,t){"use strict";t.r(n);t(32),t(10),t(44);var o={props:{selectedOption:{type:Object,required:!0},options:{type:Array,required:!0}},data:function(){return{showOptionsSelector:!1}},computed:{filteredOptions:function(){var e=this;return this.options.filter((function(n){return n.name!==e.selectedOption.name}))}},methods:{openSelector:function(){this.showOptionsSelector=!this.showOptionsSelector},selectOption:function(option){this.$emit("selectOption",option),this.showOptionsSelector=!1},onClickOutside:function(){this.showOptionsSelector=!1}}},r=(t(721),t(42)),component=Object(r.a)(o,(function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",{staticClass:"selector"},[e.filteredOptions.length?t("p",{staticClass:"selector__header",on:{click:e.openSelector}},[e._v("\n    "+e._s(e.selectedOption.name)+"\n  ")]):t("p",[e._v(e._s(e.selectedOption.name))]),e._v(" "),t("transition",{attrs:{name:"fade"}},[e.showOptionsSelector?t("ul",{directives:[{name:"click-outside",rawName:"v-click-outside",value:e.onClickOutside,expression:"onClickOutside"}],staticClass:"selector__body"},e._l(e.filteredOptions,(function(option){return t("li",{key:option.id},[t("a",{attrs:{href:"#"},on:{click:function(n){return n.preventDefault(),e.selectOption(option)}}},[e._v(e._s(option.name))])])})),0):e._e()])],1)}),[],!1,null,"07fc1970",null);n.default=component.exports},930:function(e,n,t){var content=t(1036);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(81).default)("759218a0",content,!0,{sourceMap:!1})}}]);