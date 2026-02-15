# TODO — Classic Chicago Magazine

## High Priority
- [ ] Disable Vercel Deployment Protection so preview URLs are publicly accessible (Settings → Deployment Protection)
- [ ] Confirm Formsubmit activation emails for `subscribe@2ccmag.com` and `advertise@2ccmag.com`, then re-enable forms
- [x] Scheduled deploy to production: Saturday Feb 14 at 11:30pm CST (GitHub Actions workflow in place)

## Cleanup
- [ ] Remove experimental homepage variants from dev/dev2: `index-b1.html`, `index-b2.html`, `index-b3.html`, `index-b4.html`, `index-b.html`, `index-c.html`
- [ ] Decide whether to keep or remove the edition test page (`editions/2026-02-15/index.html`)
- [ ] Review Feb 08 edition articles for nav consistency and content quality
- [ ] Update Children's Ball placeholder on edition page (`editions/2026-02-15/index.html`) — uses purple gradient instead of real thumbnail

## Forms
- [ ] Re-enable Subscribe form after Formsubmit activation confirmed
- [ ] Re-enable Advertise form after Formsubmit activation confirmed

## Content / Editorial
- [ ] Update `about.html` "Our Writers This Week" section each edition
- [ ] Add new articles and editions as they come in

## Infrastructure
- [ ] Remove `scheduled-deploy.yml` workflow after production deploy completes
- [ ] Consider automated link/asset checking (CI script to catch broken links and orphaned files)
- [ ] Establish ad naming convention for future advertisers in `/ads/`
