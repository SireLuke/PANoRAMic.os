# Exact Monster ordinary character-table audit using GAP + CTblLib.
# Run: gap -q -b -r scripts/monster_character_table_audit.g

if LoadPackage("ctbllib") <> true then
  Error("CTblLib is required; install GAP package gap-character-tables");
fi;

tbl := CharacterTable("M");
irr := Irr(tbl);
classNames := ClassNames(tbl);
centralizers := SizesCentralizers(tbl);
nClasses := Length(classNames);
nIrr := Length(irr);

if nClasses <> 194 or nIrr <> 194 then
  Error(Concatenation("Expected 194 Monster classes and irreducibles; got ",
    String(nClasses), " and ", String(nIrr)));
fi;

# Full ordinary-character row orthogonality: <chi_i, chi_j> = delta_ij.
rowPairs := 0;
for i in [1..nIrr] do
  for j in [1..nIrr] do
    expected := 0;
    if i = j then expected := 1; fi;
    actual := ScalarProduct(tbl, irr[i], irr[j]);
    if actual <> expected then
      Error(Concatenation("Row orthogonality failed at rows ",
        String(i), ",", String(j), ": ", String(actual)));
    fi;
    rowPairs := rowPairs + 1;
  od;
od;

# Full column orthogonality:
# sum_chi chi(g) conjugate(chi(h)) = delta_[g],[h] * |C_M(g)|.
columnPairs := 0;
for i in [1..nClasses] do
  for j in [1..nClasses] do
    actual := Sum([1..nIrr],
      k -> irr[k][i] * ComplexConjugate(irr[k][j]));
    expected := 0;
    if i = j then expected := centralizers[i]; fi;
    if actual <> expected then
      Error(Concatenation("Column orthogonality failed at classes ",
        String(i), ",", String(j), ": ", String(actual),
        " expected ", String(expected)));
    fi;
    columnPairs := columnPairs + 1;
  od;
od;

# Selected irreducibles in the graded Moonshine module through q^4.
degrees := List(irr, chi -> chi[1]);
selectedDegrees := [1, 196883, 21296876, 842609326, 19360062527];
selectedRows := List(selectedDegrees, d -> Position(degrees, d));
if ForAny(selectedRows, x -> x = fail) then
  Error("A required Monster irreducible degree is missing from CTblLib");
fi;

# q^1..q^4 multiplicities for chi_1, chi_2, chi_3, chi_4, chi_6.
multiplicities := [
  [1, 1, 0, 0, 0],
  [1, 1, 1, 0, 0],
  [2, 2, 1, 1, 0],
  [2, 3, 2, 1, 1]
];

classLabels := ["2a", "2b", "3a"];
expectedSeries := [
  [4372, 96256, 1240002, 10698752],
  [276, -2048, 11202, -49152],
  [783, 8672, 65367, 371520]
];
classPositions := List(classLabels, label -> Position(classNames, label));
if ForAny(classPositions, x -> x = fail) then
  Error(Concatenation("Missing one of required Monster classes: ",
    String(classLabels)));
fi;

traceResults := [];
for c in [1..Length(classLabels)] do
  coefficients := [];
  for qPower in [1..4] do
    value := Sum([1..Length(selectedRows)],
      j -> multiplicities[qPower][j] * irr[selectedRows[j]][classPositions[c]]);
    if not IsInt(value) then
      Error(Concatenation("Expected integral trace for class ", classLabels[c]));
    fi;
    if value <> expectedSeries[c][qPower] then
      Error(Concatenation("McKay-Thompson trace mismatch for ",
        classLabels[c], " q^", String(qPower), ": ",
        String(value), " expected ", String(expectedSeries[c][qPower])));
    fi;
    Add(coefficients, value);
  od;
  Add(traceResults, coefficients);
od;

# Check the Leech/Conway side of the involution centralizer dictionary.
co1 := CharacterTable("Co1");
baby := CharacterTable("B");
pos2a := classPositions[1];
pos2b := classPositions[2];
if centralizers[pos2a] <> 2 * Size(baby) then
  Error("Monster 2A centralizer order is not 2*|Baby Monster|");
fi;
if centralizers[pos2b] <> 2^25 * Size(co1) then
  Error("Monster 2B centralizer order is not 2^25*|Co1|");
fi;
co0Order := 2 * Size(co1);

Print("MONSTER_CHARACTER_TABLE_AUDIT_OK\n");
Print("classes=", nClasses, " irreducibles=", nIrr,
  " row_pairs=", rowPairs, " column_pairs=", columnPairs, "\n");
Print("2A_q1_to_q4=", traceResults[1], "\n");
Print("2B_q1_to_q4=", traceResults[2], "\n");
Print("3A_q1_to_q4=", traceResults[3], "\n");
Print("Co1_order=", Size(co1), " Co0_order_from_2.Co1=", co0Order, "\n");
Print("centralizer_2A=", centralizers[pos2a],
  " centralizer_2B=", centralizers[pos2b], "\n");
Print("LEECH_MONSTER_INVOLUTION_BRIDGE_OK\n");
QUIT;
