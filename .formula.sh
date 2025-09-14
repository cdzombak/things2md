#!/usr/bin/env bash
set -euo pipefail

if [ -z "$FORMULA_VERSION_NO_V" ]; then
  echo "missing FORUMLA_VERSION_NO_V"
  exit 1
fi
if [ -z "$FORMULA_TGZ_SHA256" ]; then
  echo "missing FORMULA_TGZ_SHA256"
  exit 1
fi

cat <<EOF
# typed: true
# frozen_string_literal: true

# This file was automatically generated. DO NOT EDIT.
class Things2md < Formula
  desc "Export Things 3 projects to Markdown"
  homepage "https://github.com/cdzombak/things2md"
  url "https://github.com/cdzombak/things2md/releases/download/v${FORMULA_VERSION_NO_V}/things2md-${FORMULA_VERSION_NO_V}-all.tar.gz"
  sha256 "${FORMULA_TGZ_SHA256}"
  license "LGPL-3.0"

  def install
    bin.install "things2md"
  end

  test do
    assert_match("${FORMULA_VERSION_NO_V}", shell_output("#{bin}/things2md --version"))
  end
end
EOF
