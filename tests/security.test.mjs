import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const source = readFileSync(new URL("../contracts/VerifiableServiceSettlement.py", import.meta.url), "utf8");

test("validators independently fetch committed evidence", () => {
  assert.match(source, /gl\.nondet\.web\.get\(urls\[index\]\)/);
  assert.match(source, /digest == expected_hashes\[index\]/);
  assert.match(source, /not _is_sha256\(expected_sha256\)/);
  assert.match(source, /independent = observe\(\)/);
});

test("decision-bearing report requires exact equality", () => {
  assert.match(source, /"semantic", "observed_hashes", "hash_matches", "authorities"/);
  assert.match(source, /all\(leader\.calldata\.get\(key\) == independent\[key\]/);
  assert.doesNotMatch(source, /confidence/);
});

test("settlement transfers locked credits", () => {
  assert.match(source, /self\.balances\[job\.provider\].*\+ job\.amount/);
  assert.match(source, /job\.status = SETTLED/);
  assert.match(source, /job\.status not in \(ACCEPTED, EVIDENCE_BOUND\)/);
});
