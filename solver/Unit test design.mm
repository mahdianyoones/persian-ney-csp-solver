<map version="freeplane 1.7.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="Units of system&apos;s behavior" FOLDED="false" ID="ID_763706885" CREATED="1661000376595" MODIFIED="1661083611091" STYLE="oval">
<font SIZE="18"/>
<hook NAME="MapStyle" zoom="2.0">
    <properties edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" show_note_icons="true" fit_to_viewport="false"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24.0 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ICON_SIZE="12.0 pt" COLOR="#000000" STYLE="fork">
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important">
<icon BUILTIN="yes"/>
</stylenode>
<stylenode TEXT="Simple behavior" COLOR="#33cc00"/>
<stylenode TEXT="Semi-complex behavior" COLOR="#ff9900">
<font SIZE="10"/>
</stylenode>
<stylenode TEXT="Complex behavior" COLOR="#ff3300">
<font SIZE="10"/>
</stylenode>
<stylenode TEXT="Behavior details" COLOR="#999999">
<font SIZE="7"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10.0 pt" SHAPE_VERTICAL_MARGIN="10.0 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="94" RULE="ON_BRANCH_CREATION"/>
<node TEXT="Initializes the domains of variables" POSITION="right" ID="ID_187230688" CREATED="1661599891025" MODIFIED="1661601249739">
<icon BUILTIN="button_ok"/>
<edge COLOR="#0000ff"/>
</node>
<node TEXT="makes the domain of variables unary consistent" POSITION="right" ID="ID_869327062" CREATED="1661600923213" MODIFIED="1661601283972">
<icon BUILTIN="button_ok"/>
<edge COLOR="#7c0000"/>
</node>
<node TEXT="hole1A constraint behaviors" FOLDED="true" POSITION="right" ID="ID_523386345" CREATED="1662028600772" MODIFIED="1663579619608">
<icon BUILTIN="button_ok"/>
<edge COLOR="#7c7c00"/>
<node TEXT="a partition is a system behavior that is performed for a range of values for an input" ID="ID_1031861582" CREATED="1662028620766" MODIFIED="1662368349727"/>
<node TEXT="behavior granularity" ID="ID_1338726603" CREATED="1662369266046" MODIFIED="1662369296404">
<node TEXT="Note: we define a partition W.R.T. the boundaries of one variable only" ID="ID_1491432467" CREATED="1662368316905" MODIFIED="1662368358376"/>
<node TEXT="The number of combinations of input/value pairs are limited, so testing all these combinations separately is not costly" ID="ID_1647305886" CREATED="1662368358612" MODIFIED="1662368736155"/>
<node TEXT="For example, one of the module&apos;s behaviors is that it examines L1&apos;s upper bound and figures out it is consistent and leaves it alone" ID="ID_351354488" CREATED="1662368752437" MODIFIED="1662368798351"/>
<node TEXT="This be behavior is done by the module in various cases; for example, the module might examine the consistency of L2 and L1 simultaneously and treat L1 the same regardless of the way it treats L2" ID="ID_1444926348" CREATED="1662368799759" MODIFIED="1662368880378"/>
<node TEXT="We consider for the latter case different units of behavior; for instance, one behavior is that the systems examines L1 and L2 and leaves L1 alone since it is already consistent, but it reduces the domain of L2." ID="ID_13004349" CREATED="1662368889290" MODIFIED="1662368991555"/>
<node TEXT="In another behavior, the module examines L1 and L2 and reduces the domain of both" ID="ID_79945972" CREATED="1662368991825" MODIFIED="1662369020098"/>
<node TEXT="Therefore, behaviors are fine-grained and have a relatively high degree of granularity" ID="ID_1220560542" CREATED="1662369022379" MODIFIED="1662369061542"/>
</node>
<node TEXT="inputs and values" FOLDED="true" ID="ID_1174114990" CREATED="1662099413350" MODIFIED="1662099524776">
<node TEXT="curvar" ID="ID_1354758013" CREATED="1662099415932" MODIFIED="1662099420188">
<node TEXT="L1" ID="ID_476981679" CREATED="1662099516876" MODIFIED="1662099517696"/>
<node TEXT="L2" ID="ID_1386705021" CREATED="1662099518097" MODIFIED="1662099518845"/>
<node TEXT="L3" ID="ID_1853557078" CREATED="1662099519421" MODIFIED="1662099520138"/>
</node>
<node TEXT="value" ID="ID_1681507713" CREATED="1662099420377" MODIFIED="1662099422532">
<node TEXT="an integer" ID="ID_1975134759" CREATED="1662099527786" MODIFIED="1662099534633"/>
<node TEXT="empty" ID="ID_688125658" CREATED="1662099534897" MODIFIED="1662099545035"/>
</node>
<node TEXT="A[L1]" ID="ID_1406047119" CREATED="1662099422746" MODIFIED="1662099432351">
<node TEXT="an integer" ID="ID_1432246689" CREATED="1662099546628" MODIFIED="1662099552434"/>
<node TEXT="empty" ID="ID_1608429530" CREATED="1662099552675" MODIFIED="1662099555195"/>
</node>
<node TEXT="A[L2]" ID="ID_216243593" CREATED="1662099422746" MODIFIED="1662099439294">
<node TEXT="an integer" ID="ID_118917750" CREATED="1662099546628" MODIFIED="1662099552434"/>
<node TEXT="empty" ID="ID_1115654492" CREATED="1662099552675" MODIFIED="1662099555195"/>
</node>
<node TEXT="A[L3]" ID="ID_1337542701" CREATED="1662099422746" MODIFIED="1662099440814">
<node TEXT="an integer" ID="ID_154241386" CREATED="1662099546628" MODIFIED="1662099552434"/>
<node TEXT="empty" ID="ID_882505269" CREATED="1662099552675" MODIFIED="1662099555195"/>
</node>
<node TEXT="D[L1][min]" ID="ID_291871144" CREATED="1662099444004" MODIFIED="1662099449861">
<node TEXT="an integer" ID="ID_1640676567" CREATED="1662099546628" MODIFIED="1662099552434"/>
</node>
<node TEXT="D[L1][max]" ID="ID_543314474" CREATED="1662099444004" MODIFIED="1662099455377">
<node TEXT="an integer" ID="ID_1380270898" CREATED="1662099546628" MODIFIED="1662099552434"/>
</node>
<node TEXT="D[L2][min]" ID="ID_1092961238" CREATED="1662099444004" MODIFIED="1662099457994">
<node TEXT="an integer" ID="ID_878203797" CREATED="1662099546628" MODIFIED="1662099552434"/>
</node>
<node TEXT="D[L2][max]" ID="ID_18657199" CREATED="1662099444004" MODIFIED="1662099463066">
<node TEXT="an integer" ID="ID_1361425527" CREATED="1662099546628" MODIFIED="1662099552434"/>
</node>
<node TEXT="D[L3][min]" ID="ID_1127915206" CREATED="1662099444004" MODIFIED="1662099470188">
<node TEXT="an integer" ID="ID_297219344" CREATED="1662099546628" MODIFIED="1662099552434"/>
</node>
<node TEXT="D[L3][max]" ID="ID_279770066" CREATED="1662099444004" MODIFIED="1662099472991">
<node TEXT="an integer" ID="ID_492638576" CREATED="1662099546628" MODIFIED="1662099552434"/>
</node>
<node TEXT="rd[L1]" ID="ID_1891462646" CREATED="1662099476583" MODIFIED="1662099498917">
<node TEXT="set" ID="ID_1246342144" CREATED="1662099581575" MODIFIED="1662099590370"/>
<node TEXT="not set" ID="ID_1750593032" CREATED="1662099595746" MODIFIED="1662099599139"/>
</node>
<node TEXT="rd[L2]" ID="ID_623510268" CREATED="1662099476583" MODIFIED="1662099502389">
<node TEXT="set" ID="ID_1073075074" CREATED="1662099581575" MODIFIED="1662099590370"/>
<node TEXT="not set" ID="ID_113395449" CREATED="1662099595746" MODIFIED="1662099599139"/>
</node>
<node TEXT="rd[L3]" ID="ID_345574464" CREATED="1662099476583" MODIFIED="1662099507534">
<node TEXT="set" ID="ID_1355445654" CREATED="1662099581575" MODIFIED="1662099590370"/>
<node TEXT="not set" ID="ID_776926074" CREATED="1662099595746" MODIFIED="1662099599139"/>
</node>
</node>
<node TEXT="Module&apos;s behaviors for one variable" ID="ID_1967559030" CREATED="1662036184975" MODIFIED="1662369167920">
<node ID="ID_559524905" CREATED="1662099206748" MODIFIED="1662367083759"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      <b>1.</b>&#160;the upper bound on the domain of a variable is consistent hence no reduction is needed
    </p>
  </body>
</html>
</richcontent>
</node>
<node ID="ID_1407045773" CREATED="1662099223676" MODIFIED="1662367125582"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      <b>2.</b>&#160;the upper bound on the domain of a variable is inconsistent, but reduction <u>is</u>&#160;possible
    </p>
  </body>
</html>
</richcontent>
</node>
<node ID="ID_494703958" CREATED="1662099304778" MODIFIED="1662367121608"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      <b>3.</b>&#160;the upper bound on the domain of a variable is inconsistent and reduction <u>is not</u>&#160;possible
    </p>
  </body>
</html>
</richcontent>
</node>
</node>
<node TEXT="Behavior 1 example" ID="ID_1907467289" CREATED="1662369181310" MODIFIED="1662369649570">
<node TEXT="representative input/value pairs" ID="ID_1673778859" CREATED="1662369688861" MODIFIED="1662369978538">
<node TEXT="D[L1][max] = 100" ID="ID_605510003" CREATED="1662369694731" MODIFIED="1662369736687"/>
<node TEXT="curvar = L2" ID="ID_1959632278" CREATED="1662369781065" MODIFIED="1662369784396"/>
<node TEXT="value" ID="ID_340352651" CREATED="1662369719342" MODIFIED="1662369721575">
<node TEXT="100" OBJECT="java.lang.Long|100" ID="ID_1164609964" CREATED="1662369757060" MODIFIED="1662369758100"/>
</node>
<node TEXT="A[L3]" ID="ID_1799744148" CREATED="1662369723727" MODIFIED="1662369727090">
<node TEXT="122" OBJECT="java.lang.Long|122" ID="ID_733925062" CREATED="1662369759437" MODIFIED="1662369760490"/>
</node>
<node TEXT="other inputs are None" ID="ID_1855196734" CREATED="1662369798685" MODIFIED="1662369808797"/>
</node>
<node TEXT="relationship between inputs" ID="ID_246637797" CREATED="1662367596057" MODIFIED="1662369672341">
<node TEXT="D[L1][max] &lt; h1 - value - A[L3] - 10" ID="ID_1527963527" CREATED="1662367356939" MODIFIED="1662367471281"/>
<node TEXT="100 &lt; 99" ID="ID_77153237" CREATED="1662369849035" MODIFIED="1662369956347"/>
</node>
<node TEXT="equivalence partitioning explanation" ID="ID_295986611" CREATED="1662370061866" MODIFIED="1662370080835">
<node ID="ID_1205308426" CREATED="1662369980208" MODIFIED="1662370227187"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      note that that module needs to reach
    </p>
    <p>
      <b>100 &lt;&#160;&#160;some_value_lower_than_100 </b>
    </p>
    <p>
      to behave this way (finds L1 consistent)
    </p>
  </body>
</html>
</richcontent>
</node>
<node ID="ID_514505365" CREATED="1662370083617" MODIFIED="1662370138240"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      and so many values for <b>&quot;value&quot;</b>&#160;and &quot;<b>A[L3]&quot;</b>&#160; inputs can yield the same result
    </p>
  </body>
</html>
</richcontent>
</node>
<node TEXT="however, we only need to test the system for this behavior for one such case" ID="ID_1983954949" CREATED="1662370139330" MODIFIED="1662370197845"/>
</node>
</node>
<node TEXT="an exhaustive list of input/value pairs for all the behaviors exists in the spreadsheet file" ID="ID_1894827464" CREATED="1662369229499" MODIFIED="1662370258732"/>
</node>
<node TEXT="hole1B constraint behaviors" POSITION="right" ID="ID_1105655473" CREATED="1663579548170" MODIFIED="1663579624145">
<icon BUILTIN="button_ok"/>
<edge COLOR="#ff0000"/>
</node>
<node TEXT="hole2 constraint behaviors" POSITION="right" ID="ID_5459536" CREATED="1663579635716" MODIFIED="1663583858813">
<icon BUILTIN="button_ok"/>
<edge COLOR="#0000ff"/>
</node>
<node TEXT="hole3 constraint behaviors" POSITION="right" ID="ID_791782754" CREATED="1663583859602" MODIFIED="1663761732211">
<icon BUILTIN="button_ok"/>
<edge COLOR="#00ff00"/>
</node>
<node TEXT="hole4 constraint behaviors" POSITION="right" ID="ID_1578395523" CREATED="1663761738779" MODIFIED="1663761765966">
<icon BUILTIN="button_ok"/>
<edge COLOR="#ff00ff"/>
</node>
<node TEXT="hole5 constraint behaviors" POSITION="right" ID="ID_1883075035" CREATED="1663761740643" MODIFIED="1663761765971">
<icon BUILTIN="button_ok"/>
<edge COLOR="#00ffff"/>
</node>
<node TEXT="hole6 constraint behaviors" POSITION="right" ID="ID_1119341886" CREATED="1663761742555" MODIFIED="1663761765971">
<icon BUILTIN="button_ok"/>
<edge COLOR="#7c0000"/>
</node>
<node TEXT="makes the boundary of variables consistent (mac.indirect)" POSITION="left" ID="ID_141201004" CREATED="1661599914505" MODIFIED="1661601295701">
<edge COLOR="#ff00ff"/>
</node>
<node TEXT="assigns a value to an unassigned variable" POSITION="left" ID="ID_1605713215" CREATED="1661600961655" MODIFIED="1661601087485">
<edge COLOR="#00ff00"/>
</node>
<node TEXT="backtracks to a different value" POSITION="left" ID="ID_942559200" CREATED="1661600672259" MODIFIED="1661600883093">
<edge COLOR="#00ffff"/>
</node>
<node TEXT="backjumps to a different variable" POSITION="left" ID="ID_1159595711" CREATED="1661600858887" MODIFIED="1661600879273">
<edge COLOR="#0000ff"/>
</node>
<node TEXT="terminates" POSITION="left" ID="ID_870337630" CREATED="1661600733335" MODIFIED="1661600734930">
<edge COLOR="#007c00"/>
</node>
<node TEXT="len constraint behaviors" LOCALIZED_STYLE_REF="default" POSITION="right" ID="ID_1257229158" CREATED="1661008563773" MODIFIED="1664130481979">
<icon BUILTIN="button_ok"/>
<edge COLOR="#ff0000"/>
</node>
<node TEXT="same_r constraint behaviors" LOCALIZED_STYLE_REF="default" POSITION="right" ID="ID_1030975271" CREATED="1661008563773" MODIFIED="1664134295989">
<icon BUILTIN="button_ok"/>
<edge COLOR="#00ff00"/>
</node>
<node TEXT="same_t constraint behaviors" LOCALIZED_STYLE_REF="default" POSITION="right" ID="ID_428535701" CREATED="1661008563773" MODIFIED="1664143687718">
<icon BUILTIN="button_ok"/>
<edge COLOR="#00ffff"/>
</node>
<node TEXT="d_dec constraint behaviors" LOCALIZED_STYLE_REF="default" POSITION="right" ID="ID_143389757" CREATED="1661008563773" MODIFIED="1663761803315">
<edge COLOR="#ff00ff"/>
</node>
<node TEXT="in_stock constraint behaviors" LOCALIZED_STYLE_REF="default" POSITION="right" ID="ID_10654768" CREATED="1661008563773" MODIFIED="1663761810868">
<edge COLOR="#7c0000"/>
</node>
<node TEXT="l1_half_l2 constraint behaviors" LOCALIZED_STYLE_REF="default" POSITION="right" ID="ID_1674793195" CREATED="1661008563773" MODIFIED="1663761819558">
<edge COLOR="#007c00"/>
</node>
<node TEXT="l_dec constraint behaviors" LOCALIZED_STYLE_REF="default" POSITION="right" ID="ID_1479427135" CREATED="1661008563773" MODIFIED="1663761830728">
<edge COLOR="#007c7c"/>
</node>
</node>
</map>
