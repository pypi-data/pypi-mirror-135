(window.webpackJsonp=window.webpackJsonp||[]).push([[78],{801:function(e,n,t){var content=t(893);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(81).default)("4c3d6c4d",content,!0,{sourceMap:!1})},892:function(e,n,t){"use strict";t(801)},893:function(e,n,t){var r=t(80)(!1);r.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.sidebar__view-more[data-v-f93e0f9a]{color:#4c4ea3;text-decoration:none;outline:none;margin-bottom:1.5em;display:inline-block}.info[data-v-f93e0f9a]{color:#353664;position:relative;display:flex;margin-bottom:.7em}.records-number[data-v-f93e0f9a]{margin-right:0;margin-left:auto;font-weight:700}',""]),e.exports=r},955:function(e,n,t){"use strict";t.r(n);var r=t(36),o=(t(368),t(154),t(371),{props:{limit:{type:Number,required:!0},object:{type:Object,required:!0},k:{type:String,required:!0}},computed:{sortedObject:function(){return Object.entries(this.object[this.k]).sort((function(e,n){var a=Object(r.a)(e,2)[1];return Object(r.a)(n,2)[1]-a}))}}}),c=(t(892),t(42)),component=Object(c.a)(o,(function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",[e._l(e.sortedObject.slice(0,e.limit),(function(n,r){return t("div",{key:r,staticClass:"info"},[t("label",[e._v(e._s(n[0]))]),e._v(" "),t("span",{staticClass:"records-number"},[t("strong",[e._v(e._s(e._f("formatNumber")(n[1])))])])])})),e._v(" "),0!==e.limit&&e.sortedObject.length>3?t("a",{staticClass:"sidebar__view-more",attrs:{href:"#"},on:{click:function(n){return n.preventDefault(),e.$emit("limit",e.k)}}},[e._v(e._s(3===e.limit?"view more":"view less"))]):e._e()],2)}),[],!1,null,"f93e0f9a",null);n.default=component.exports}}]);