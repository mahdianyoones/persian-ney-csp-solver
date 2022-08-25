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
<hook NAME="AutomaticEdgeColor" COUNTER="45" RULE="ON_BRANCH_CREATION"/>
<node TEXT="Simple" FOLDED="true" POSITION="right" ID="ID_1372328605" CREATED="1661088843506" MODIFIED="1661088847329">
<edge COLOR="#007c7c"/>
<node TEXT="defines CSP variables" STYLE_REF="Simple behavior" ID="ID_1910050850" CREATED="1661004517853" MODIFIED="1661088872956">
<node TEXT="28 variables" STYLE_REF="Behavior details" ID="ID_709082416" CREATED="1661004527693" MODIFIED="1661080897403">
<font ITALIC="true"/>
</node>
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1766198284" CREATED="1661081057156" MODIFIED="1661082375014">
<node TEXT="CSP" STYLE_REF="Behavior details" ID="ID_1267766328" CREATED="1661081087786" MODIFIED="1661082400124"/>
</node>
</node>
<node TEXT="defines non-unary constraints on variables" STYLE_REF="Simple behavior" ID="ID_593335993" CREATED="1661004637474" MODIFIED="1661088872959">
<node TEXT="13 constraints" STYLE_REF="Behavior details" ID="ID_1856293113" CREATED="1661006081676" MODIFIED="1661082400127">
<font ITALIC="true"/>
</node>
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1330800352" CREATED="1661081118004" MODIFIED="1661082375016">
<node TEXT="CSP" STYLE_REF="Behavior details" ID="ID_1487042533" CREATED="1661081123635" MODIFIED="1661082400127"/>
</node>
</node>
<node TEXT="initiates domains for L variables" STYLE_REF="Simple behavior" ID="ID_1311906002" CREATED="1661006882795" MODIFIED="1661088872960">
<node TEXT="initially infinite values are possible, starting from 1" STYLE_REF="Behavior details" ID="ID_1243490243" CREATED="1661006960247" MODIFIED="1661082400128">
<font ITALIC="true"/>
</node>
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1053401016" CREATED="1661081118004" MODIFIED="1661082375016">
<node TEXT="UNARY" STYLE_REF="Behavior details" ID="ID_744600115" CREATED="1661089060188" MODIFIED="1661089071177"/>
</node>
</node>
<node TEXT="adjusts bounds of L4, L5, and L6 to contain holes" STYLE_REF="Simple behavior" ID="ID_588147628" CREATED="1661004219865" MODIFIED="1661088872962">
<node TEXT="their lower bounds are adjusted" STYLE_REF="Behavior details" ID="ID_1305366168" CREATED="1661007236071" MODIFIED="1661082400129">
<font ITALIC="true"/>
</node>
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_42095033" CREATED="1661081401658" MODIFIED="1661082368941">
<node TEXT="UNARY" STYLE_REF="Behavior details" ID="ID_554851246" CREATED="1661081405427" MODIFIED="1661082400130"/>
</node>
</node>
<node TEXT="adjusts bounds of D1" STYLE_REF="Simple behavior" ID="ID_1006832333" CREATED="1661004233858" MODIFIED="1661088872964">
<node TEXT="should not be lower than 18 millimeters" STYLE_REF="Behavior details" ID="ID_1162755495" CREATED="1661007048660" MODIFIED="1661082400130">
<font ITALIC="true"/>
</node>
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1418967509" CREATED="1661081479959" MODIFIED="1661082368942">
<node TEXT="UNARY" STYLE_REF="Behavior details" ID="ID_1673936307" CREATED="1661081483876" MODIFIED="1661082400131"/>
</node>
</node>
<node TEXT="determines impacts of selecting variables" STYLE_REF="Simple behavior" ID="ID_926652828" CREATED="1661005900730" MODIFIED="1661088872966">
<node TEXT="a special heuristic" STYLE_REF="Behavior details" ID="ID_1189960919" CREATED="1661005926310" MODIFIED="1661082400131">
<font ITALIC="true"/>
</node>
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_800370589" CREATED="1661081515778" MODIFIED="1661082368944">
<node TEXT="SELECT" STYLE_REF="Behavior details" ID="ID_651147005" CREATED="1661081492749" MODIFIED="1661082400132"/>
</node>
</node>
<node TEXT="determines constraints orders" STYLE_REF="Simple behavior" ID="ID_375202397" CREATED="1661005392330" MODIFIED="1661088872967">
<node TEXT="for degree heuristic" STYLE_REF="Behavior details" ID="ID_586997352" CREATED="1661006000741" MODIFIED="1661082400133">
<font ITALIC="true"/>
</node>
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1613183362" CREATED="1661081515778" MODIFIED="1661082368946">
<node TEXT="SELECT" STYLE_REF="Behavior details" ID="ID_830382540" CREATED="1661081492749" MODIFIED="1661082400133"/>
</node>
</node>
<node TEXT="determines the degree of variables" STYLE_REF="Simple behavior" ID="ID_1728522265" CREATED="1661005817439" MODIFIED="1661088872969">
<node TEXT="for degree heuristic" STYLE_REF="Behavior details" ID="ID_445322750" CREATED="1661005860366" MODIFIED="1661082400133">
<font ITALIC="true"/>
</node>
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_365466847" CREATED="1661081515778" MODIFIED="1661082368947">
<node TEXT="SELECT" STYLE_REF="Behavior details" ID="ID_1095114722" CREATED="1661081492749" MODIFIED="1661082400134"/>
</node>
</node>
</node>
<node TEXT="Semi-complex" POSITION="right" ID="ID_1369724767" CREATED="1661088847833" MODIFIED="1661088854049">
<edge COLOR="#7c7c00"/>
<node TEXT="initiates TH, R, and D vars with existing thicknesses, roundness, and diameters respectively" STYLE_REF="Semi-complex behavior" ID="ID_795916042" CREATED="1661004260894" MODIFIED="1661088881511">
<node TEXT="systems under test" STYLE_REF="Behavior details" ID="ID_1452310273" CREATED="1661081280479" MODIFIED="1661082900482">
<node TEXT="CATALOG" STYLE_REF="Behavior details" ID="ID_1530909738" CREATED="1661081305843" MODIFIED="1661082440295"/>
</node>
<node TEXT="arrange" ID="ID_696336745" CREATED="1661163638406" MODIFIED="1661163642991">
<node TEXT="sut = CATALOG(csvfile)" ID="ID_43087914" CREATED="1661164103610" MODIFIED="1661166457073"/>
</node>
<node TEXT="act" ID="ID_1254487270" CREATED="1661163643395" MODIFIED="1661163645351">
<node TEXT="diameters = sut.values(&quot;D&quot;)" ID="ID_1392499713" CREATED="1661166432465" MODIFIED="1661166464133"/>
<node TEXT="thicknesses = sut.values(&quot;TH&quot;)" ID="ID_1423697423" CREATED="1661166432465" MODIFIED="1661166470839"/>
<node TEXT="roundnesses = sut.values(&quot;R&quot;)" ID="ID_1066024127" CREATED="1661166432467" MODIFIED="1661166482373"/>
</node>
<node TEXT="assert" ID="ID_1311562838" CREATED="1661163645650" MODIFIED="1661163648350">
<node TEXT="compare with values in the excel file" ID="ID_528885421" CREATED="1661166488008" MODIFIED="1661166501772"/>
</node>
</node>
<node TEXT="maintains direct consistency" STYLE_REF="Semi-complex behavior" ID="ID_1396638486" CREATED="1661008342854" MODIFIED="1661088881514">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_814135569" CREATED="1661081515778" MODIFIED="1661082368950">
<node TEXT="MAC" STYLE_REF="Behavior details" ID="ID_992302687" CREATED="1661081492749" MODIFIED="1661082400135"/>
</node>
</node>
<node TEXT="backjumps to an assigned variable if mac or bound propagation leads to contradiction" STYLE_REF="Semi-complex behavior" ID="ID_1529654677" CREATED="1661008501977" MODIFIED="1661088881518">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1677368872" CREATED="1661081515778" MODIFIED="1661082368952">
<node TEXT="SOLVER" STYLE_REF="Behavior details" ID="ID_184598938" CREATED="1661081492749" MODIFIED="1661082400136"/>
</node>
</node>
<node TEXT="backtracks to the previous variable and tries a different value if the domain of a selected variable is exhausted" STYLE_REF="Semi-complex behavior" ID="ID_1321351181" CREATED="1661083003754" MODIFIED="1661088881524">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_941745010" CREATED="1661081515778" MODIFIED="1661082368952">
<node TEXT="SOLVER" STYLE_REF="Behavior details" ID="ID_1180380969" CREATED="1661081492749" MODIFIED="1661082400136"/>
</node>
</node>
</node>
<node TEXT="Complex" POSITION="left" ID="ID_475799040" CREATED="1661088854599" MODIFIED="1661088856035">
<edge COLOR="#ff0000"/>
<node TEXT="establishes pre-search bound consistency for all constraints recursively" STYLE_REF="Complex behavior" ID="ID_1206298011" CREATED="1661007413571" MODIFIED="1661088897810">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1652827555" CREATED="1661081515778" MODIFIED="1661082368948">
<node TEXT="MAC" STYLE_REF="Behavior details" ID="ID_379887605" CREATED="1661081492749" MODIFIED="1661082400134"/>
</node>
</node>
<node TEXT="selects an unassigned variable and assigns a value to it" STYLE_REF="Complex behavior" ID="ID_508896924" CREATED="1661007514381" MODIFIED="1661088897813">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1860319940" CREATED="1661081515778" MODIFIED="1661082548590">
<node TEXT="SELECT" STYLE_REF="Behavior details" ID="ID_1115583745" CREATED="1661081492749" MODIFIED="1661082400135"/>
</node>
</node>
<node TEXT="applies bound propagation recursively" STYLE_REF="Complex behavior" ID="ID_1764694182" CREATED="1661008375526" MODIFIED="1661088897816">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1334838733" CREATED="1661081515778" MODIFIED="1661082368951">
<node TEXT="MAC" STYLE_REF="Behavior details" ID="ID_387102561" CREATED="1661081492749" MODIFIED="1661082400136"/>
</node>
</node>
<node TEXT="establishes h4 consistency" STYLE_REF="Complex behavior" ID="ID_985737405" CREATED="1661008563773" MODIFIED="1661088969750">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_348931162" CREATED="1661081515778" MODIFIED="1661082368957">
<node TEXT="HOLE4" STYLE_REF="Behavior details" ID="ID_517482737" CREATED="1661081492749" MODIFIED="1661083473202"/>
</node>
</node>
<node TEXT="performs h4 bound propagation" STYLE_REF="Complex behavior" ID="ID_556210551" CREATED="1661080399449" MODIFIED="1661088969753">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_218129371" CREATED="1661081515778" MODIFIED="1661082368957">
<node TEXT="HOLE4" STYLE_REF="Behavior details" ID="ID_729341350" CREATED="1661081492749" MODIFIED="1661083475821"/>
</node>
</node>
<node TEXT="establishes h5 consistency" STYLE_REF="Complex behavior" ID="ID_1701647875" CREATED="1661008563773" MODIFIED="1661088969755">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_423279036" CREATED="1661081515778" MODIFIED="1661082368958">
<node TEXT="HOLE5" STYLE_REF="Behavior details" ID="ID_1246234603" CREATED="1661081492749" MODIFIED="1661083478887"/>
</node>
</node>
<node TEXT="performs h5 bound propagation" STYLE_REF="Complex behavior" ID="ID_63723952" CREATED="1661080404779" MODIFIED="1661088969757">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_867601530" CREATED="1661081515778" MODIFIED="1661082368959">
<node TEXT="HOLE5" STYLE_REF="Behavior details" ID="ID_375062211" CREATED="1661081492749" MODIFIED="1661083481921"/>
</node>
</node>
<node TEXT="establishes h6 consistency" STYLE_REF="Complex behavior" ID="ID_288294010" CREATED="1661008563773" MODIFIED="1661088969759">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_667881805" CREATED="1661081515778" MODIFIED="1661082368960">
<node TEXT="HOLE6" STYLE_REF="Behavior details" ID="ID_1272057158" CREATED="1661081492749" MODIFIED="1661083484791"/>
</node>
</node>
<node TEXT="performs h6 bound propagation" STYLE_REF="Complex behavior" ID="ID_283116556" CREATED="1661080409538" MODIFIED="1661088969761">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_884737623" CREATED="1661081515778" MODIFIED="1661082368961">
<node TEXT="HOLE6" STYLE_REF="Behavior details" ID="ID_1854694181" CREATED="1661081492749" MODIFIED="1661083496256"/>
</node>
</node>
<node TEXT="establishes d_dec consistency" STYLE_REF="Complex behavior" ID="ID_143389757" CREATED="1661008563773" MODIFIED="1661088969763">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_505925292" CREATED="1661081515778" MODIFIED="1661082368962">
<node TEXT="D_DEC" STYLE_REF="Behavior details" ID="ID_1936436454" CREATED="1661081492749" MODIFIED="1661082400144"/>
</node>
</node>
<node TEXT="performs d_dec bound propagation" STYLE_REF="Complex behavior" ID="ID_1152814088" CREATED="1661080419926" MODIFIED="1661088969765">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_489531157" CREATED="1661081515778" MODIFIED="1661082368962">
<node TEXT="D_DEC" STYLE_REF="Behavior details" ID="ID_705553655" CREATED="1661081492749" MODIFIED="1661082400145"/>
</node>
</node>
<node TEXT="establishes in_stock consistency" STYLE_REF="Complex behavior" ID="ID_10654768" CREATED="1661008563773" MODIFIED="1661088969768">
<node TEXT="systems under test" STYLE_REF="Behavior details" ID="ID_631437393" CREATED="1661081515778" MODIFIED="1661083085204">
<node TEXT="IN_STOCK" STYLE_REF="Behavior details" ID="ID_1861009637" CREATED="1661081492749" MODIFIED="1661082400146"/>
<node TEXT="CATALOG" STYLE_REF="Behavior details" ID="ID_1128411730" CREATED="1661083089271" MODIFIED="1661083540965"/>
</node>
</node>
<node TEXT="performs in_stock bound propagation" STYLE_REF="Complex behavior" ID="ID_1477217227" CREATED="1661080430340" MODIFIED="1661088969770">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1564903827" CREATED="1661081515778" MODIFIED="1661082368964">
<node TEXT="IN_STOCK" STYLE_REF="Behavior details" ID="ID_276021303" CREATED="1661081492749" MODIFIED="1661082400147"/>
<node TEXT="CATALOG" STYLE_REF="Behavior details" ID="ID_448002893" CREATED="1661083095650" MODIFIED="1661083540968"/>
</node>
</node>
<node TEXT="establishes l1_half_l2 consistency" STYLE_REF="Complex behavior" ID="ID_1674793195" CREATED="1661008563773" MODIFIED="1661088969772">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_241900961" CREATED="1661081515778" MODIFIED="1661082368965">
<node TEXT="HALF" STYLE_REF="Behavior details" ID="ID_1648271727" CREATED="1661081492749" MODIFIED="1661083329215"/>
</node>
</node>
<node TEXT="performs l1_half_l2 bound propagation" STYLE_REF="Complex behavior" ID="ID_382016572" CREATED="1661080437690" MODIFIED="1661088969774">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1364927896" CREATED="1661081515778" MODIFIED="1661082368966">
<node TEXT="HALF" STYLE_REF="Behavior details" ID="ID_1954328719" CREATED="1661081492749" MODIFIED="1661083329215"/>
</node>
</node>
<node TEXT="establishes l_dec consistency" STYLE_REF="Complex behavior" ID="ID_1479427135" CREATED="1661008563773" MODIFIED="1661088969776">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_317642244" CREATED="1661081515778" MODIFIED="1661082368967">
<node TEXT="L_DEC" STYLE_REF="Behavior details" ID="ID_895917785" CREATED="1661081492749" MODIFIED="1661082400148"/>
</node>
</node>
<node TEXT="performs l_dec bound propagation" STYLE_REF="Complex behavior" ID="ID_145873040" CREATED="1661080448082" MODIFIED="1661088969778">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_177436023" CREATED="1661081515778" MODIFIED="1661082368968">
<node TEXT="L_DEC" STYLE_REF="Behavior details" ID="ID_48857563" CREATED="1661081492749" MODIFIED="1661082400148"/>
</node>
</node>
<node TEXT="establishes len consistency" STYLE_REF="Complex behavior" ID="ID_1257229158" CREATED="1661008563773" MODIFIED="1661088969781">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_426956707" CREATED="1661081515778" MODIFIED="1661082368972">
<node TEXT="LEN" STYLE_REF="Behavior details" ID="ID_913935454" CREATED="1661081492749" MODIFIED="1661082400149"/>
</node>
</node>
<node TEXT="performs len bound propagation" STYLE_REF="Complex behavior" ID="ID_138805443" CREATED="1661080455207" MODIFIED="1661088969783">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1130623840" CREATED="1661081515778" MODIFIED="1661082368972">
<node TEXT="LEN" STYLE_REF="Behavior details" ID="ID_590118851" CREATED="1661081492749" MODIFIED="1661082400149"/>
</node>
</node>
<node TEXT="establishes same_r consistency" STYLE_REF="Complex behavior" ID="ID_1030975271" CREATED="1661008563773" MODIFIED="1661088969785">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1796268695" CREATED="1661081515778" MODIFIED="1661082368971">
<node TEXT="SAME_R" STYLE_REF="Behavior details" ID="ID_602867515" CREATED="1661081492749" MODIFIED="1661082400150"/>
</node>
</node>
<node TEXT="performs same_r bound propagation" STYLE_REF="Complex behavior" ID="ID_1596898600" CREATED="1661080462313" MODIFIED="1661088969787">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_641179063" CREATED="1661081515778" MODIFIED="1661082368970">
<node TEXT="SAME_R" STYLE_REF="Behavior details" ID="ID_1259751097" CREATED="1661081492749" MODIFIED="1661082400150"/>
</node>
</node>
<node TEXT="establishes same_th consistency" STYLE_REF="Complex behavior" ID="ID_428535701" CREATED="1661008563773" MODIFIED="1661088969789">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1275743405" CREATED="1661081515778" MODIFIED="1661082368969">
<node TEXT="SAME_TH" STYLE_REF="Behavior details" ID="ID_1519936074" CREATED="1661081492749" MODIFIED="1661082400151"/>
</node>
</node>
<node TEXT="performs same_th bound propagation" STYLE_REF="Complex behavior" ID="ID_1837953714" CREATED="1661080467254" MODIFIED="1661088969791">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_772618633" CREATED="1661081515778" MODIFIED="1661082368968">
<node TEXT="SAME_TH" STYLE_REF="Behavior details" ID="ID_380451623" CREATED="1661081492749" MODIFIED="1661082400151"/>
</node>
</node>
<node TEXT="establishes h1 consistency" STYLE_REF="Complex behavior" ID="ID_1530979961" CREATED="1661008563773" MODIFIED="1661088969793">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1225145090" CREATED="1661081515778" MODIFIED="1661082368952">
<node TEXT="HOLE1" STYLE_REF="Behavior details" ID="ID_1120497440" CREATED="1661081492749" MODIFIED="1661083385643"/>
</node>
</node>
<node TEXT="performs h1 bound propagation" STYLE_REF="Complex behavior" ID="ID_1466520120" CREATED="1661079171208" MODIFIED="1661088969795">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_949722695" CREATED="1661081515778" MODIFIED="1661082368953">
<node TEXT="HOLE1" STYLE_REF="Behavior details" ID="ID_503966401" CREATED="1661081492749" MODIFIED="1661083388351"/>
</node>
</node>
<node TEXT="establishes h2 consistency" STYLE_REF="Complex behavior" ID="ID_754624275" CREATED="1661008563773" MODIFIED="1661088969797">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_803308276" CREATED="1661081515778" MODIFIED="1661082368953">
<node TEXT="HOLE2" STYLE_REF="Behavior details" ID="ID_94206803" CREATED="1661081492749" MODIFIED="1661083460352"/>
</node>
</node>
<node TEXT="performs h2 bound propagation" STYLE_REF="Complex behavior" ID="ID_1373024645" CREATED="1661080378508" MODIFIED="1661088969799">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1462841232" CREATED="1661081515778" MODIFIED="1661082368954">
<node TEXT="HOLE2" STYLE_REF="Behavior details" ID="ID_1658773322" CREATED="1661081492749" MODIFIED="1661083464571"/>
</node>
</node>
<node TEXT="establishes h3 consistency" STYLE_REF="Complex behavior" ID="ID_263837726" CREATED="1661008563773" MODIFIED="1661088969801">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_801988890" CREATED="1661081515778" MODIFIED="1661082368955">
<node TEXT="HOLE3" STYLE_REF="Behavior details" ID="ID_18925951" CREATED="1661081492749" MODIFIED="1661083467359"/>
</node>
</node>
<node TEXT="performs h3 bound propagation" STYLE_REF="Complex behavior" ID="ID_451919333" CREATED="1661080392177" MODIFIED="1661088969803">
<node TEXT="system under test" STYLE_REF="Behavior details" ID="ID_1752414059" CREATED="1661081515778" MODIFIED="1661082368956">
<node TEXT="HOLE3" STYLE_REF="Behavior details" ID="ID_469693621" CREATED="1661081492749" MODIFIED="1661083470497"/>
</node>
</node>
</node>
</node>
</map>
