# Minimal Gemfile for `bundle exec jekyll build` (route a).
# Pinned toolchain per https://pages.github.com/versions.json, confirmed on 2026-09-06 (see
# web-static-build skill): jekyll 3.10.0, github-pages gem 232, ruby 3.3.4.
#
# 2026-09-06 build note (this machine): the full `github-pages` meta-gem (~> 232) requires
# nokogiri >= 1.16.2, which itself requires Ruby >= 3.0. This machine's only available Ruby is the
# system 2.6.10 (no rbenv/rvm/asdf installed to get a newer one). So `bundle install` with the
# meta-gem fails to resolve here — NOT a code defect, an environment ceiling. This Gemfile
# instead pins the individual pieces the meta-gem bundles that this site actually uses
# (jekyll + jekyll-seo-tag + jekyll-sitemap, at their github-pages-232-pinned versions), which
# have no nokogiri dependency and install cleanly on Ruby 2.6. GitHub Pages itself still builds
# with the real meta-gem — this is a local-only substitute so a build can be verified on this
# machine; re-attempt with the full Gemfile above if a newer local Ruby (>=3.0, <3.2) is ever
# available, per web-static-build's own "Common mistakes" table.

source "https://rubygems.org"

gem "jekyll", "3.10.0"
gem "jekyll-seo-tag"
gem "jekyll-sitemap"
gem "kramdown-parser-gfm"  # jekyll defaults kramdown's `input:` to GFM; not pulled in by kramdown itself
gem "webrick"   # jekyll 3.x + Ruby >= 3.0 needs this explicitly; harmless on 2.6, kept for parity
gem "ffi", "< 1.17"  # jekyll-watch's transitive dep; 1.17.x dropped Ruby < 3.0, same ceiling as nokogiri above
