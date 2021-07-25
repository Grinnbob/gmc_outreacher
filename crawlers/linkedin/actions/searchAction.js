const selectors = require("../selectors")
const action = require("./action.js")
const utils = require("./utils.js")

const MyExceptions = require("../../exceptions/exceptions.js")
var log = require("loglevel").getLogger("o24_logger")

class SearchAction extends action.Action {
    constructor(cookies, credentials_id, searchUrl, interval_pages) {
        super(cookies, credentials_id)

        this.searchUrl = searchUrl
        this.interval_pages = interval_pages
    }

    async search() {
        if (!this.searchUrl) {
            throw new Error("Empty search url.")
        }

        if (this.interval_pages == null || this.interval_pages < 1) {
            throw new Error("Incorrect interval_pages:", this.interval_pages)
        }

        await super.gotoChecker(this.searchUrl)

        let currentPage = 1
        let result_data = {
            code: 0,
            if_true: true,
            data: {
                arr: [],
                link: this.searchUrl,
            },
        }

        try {
            let mySelectors = {
                SEARCH_ELEMENT_SELECTOR: selectors.SEARCH_ELEMENT_SELECTOR,
                LINK_SELECTOR: selectors.LINK_SELECTOR,
                FULL_NAME_SELECTOR: selectors.FULL_NAME_SELECTOR,
                DEGREE_SELECTOR: selectors.DEGREE_SELECTOR,
                SEARCH_JOB_SELECTOR: selectors.SEARCH_JOB_SELECTOR,
                SEARCH_LOCATION_SELECTOR: selectors.SEARCH_LOCATION_SELECTOR,
                MEMBER_NAME_SELECTOR: selectors.MEMBER_NAME_SELECTOR,
            }

            while (currentPage <= this.interval_pages) {
                await utils.autoScroll(this.page)

                // wait selector here
                //await super.check_success_selector(selectors.SEARCH_ELEMENT_SELECTOR, this.page);

                if (
                    (await this.page.$(selectors.SEARCH_ELEMENT_SELECTOR)) ==
                    null
                ) {
                    // TODO: add check-selector for BAN page
                    // perhaps it was BAN
                    result_data.code = MyExceptions.SearchActionError().code
                    result_data.raw = MyExceptions.SearchActionError(
                        "something went wrong - SEARCH_ELEMENT_SELECTOR not found! page.url: " +
                            this.page.url()
                    ).error
                    log.error(
                        "SearchAction: something went wrong - SEARCH_ELEMENT_SELECTOR not found! page.url: ",
                        this.page.url()
                    )
                    break
                }

                let newData = await this.page.evaluate((mySelectors) => {
                    let results = []
                    let items = document.querySelectorAll(
                        mySelectors.SEARCH_ELEMENT_SELECTOR
                    )

                    for (let item of items) {
                        // don't add: noName LinkedIn members and 1st degree connections
                        if (
                            item.querySelector(mySelectors.LINK_SELECTOR) !=
                                null &&
                            !item
                                .querySelector(mySelectors.MEMBER_NAME_SELECTOR)
                                .innerText.toLowerCase()
                                .includes("linkedin") 
                            //     &&
                            // (item.querySelector(mySelectors.DEGREE_SELECTOR) ==
                            //     null ||
                            //     !item
                            //         .querySelector(mySelectors.DEGREE_SELECTOR)
                            //         .innerText.includes("1"))
                        ) {
                            let full_name = item.querySelector(
                                mySelectors.FULL_NAME_SELECTOR
                            )
                            let full_job = item.querySelector(
                                mySelectors.SEARCH_JOB_SELECTOR
                            )
                            let location = item.querySelector(
                                mySelectors.SEARCH_LOCATION_SELECTOR
                            )

                            let result = {
                                linkedin: "",
                                first_name: "",
                                last_name: "",
                                job_title: "",
                                company_name: "",
                                location: "",
                            }

                            result.linkedin = item.querySelector(
                                mySelectors.LINK_SELECTOR
                            ).href

                            if (location != null) {
                                result.location = location.innerText
                            }

                            if (full_name != null) {
                                full_name = full_name.innerText
                                if (full_name.includes(" ")) {
                                    result.first_name = full_name.substr(
                                        0,
                                        full_name.indexOf(" ")
                                    )
                                    result.last_name = full_name.substr(
                                        full_name.indexOf(" ") + 1
                                    )
                                } else {
                                    result.first_name = full_name
                                }
                            }

                            if (full_job != null) {
                                full_job = full_job.innerText // -> "Текущая должность: Product Marketing Manager – Morningstar"
                                //full_job = full_job.split(': ')[1]  // -> "Product Marketing Manager – Morningstar"
                                if (full_job.includes(" at ")) {
                                    result.job_title = full_job.substr(
                                        0,
                                        full_job.indexOf(" at ")
                                    ) // -> "Product Marketing Manager "
                                    result.company_name = full_job.substr(
                                        full_job.indexOf(" at ") + 4
                                    ) // -> "Morningstar"
                                } else if (full_job.includes(" - ")) {
                                    result.job_title = full_job.substr(
                                        0,
                                        full_job.indexOf(" - ")
                                    ) // -> "Product Marketing Manager "
                                    result.company_name = full_job.substr(
                                        full_job.indexOf(" - ") + 4
                                    ) // -> "Morningstar"
                                } else {
                                    result.job_title = full_job // ? or new param
                                }
                            }

                            results.push(result)
                        }
                    }
                    return results
                }, mySelectors)
                result_data.data.arr = result_data.data.arr.concat(newData)
                result_data.data.link = this.page.url()

                if ((await this.page.$(selectors.NEXT_PAGE_SELECTOR)) == null) {
                    // TODO: add check-selector for BAN page
                    // perhaps it was BAN
                    result_data.code = MyExceptions.SearchActionError().code
                    result_data.raw = MyExceptions.SearchActionError(
                        "something went wrong - NEXT_PAGE_SELECTOR not found! page.url: " +
                            this.page.url()
                    ).error
                    log.error(
                        "SearchAction: something went wrong - NEXT_PAGE_SELECTOR not found! page.url: ",
                        this.page.url()
                    )
                    break
                }

                // wait selector here
                //await super.check_success_selector(selectors.NEXT_PAGE_SELECTOR, this.page, result_data);

                if (
                    (await this.page.$(selectors.NEXT_PAGE_MUTED_SELECTOR)) !=
                    null
                ) {
                    // all awailable pages has been scribed
                    result_data.code = 1000
                    log.debug(
                        "SearchAction: All awailable pages has been scribed!"
                    )
                    break
                }

                await super.gotoChecker(utils.getNextPageURL(this.page.url()))
                //await this.page.click(selectors.NEXT_PAGE_SELECTOR)
                await this.page.waitFor(2000) // critical here!?
                await utils.update_cookie(this.page, this.credentials_id)

                // here we have to check BAN page
                result_data.data.link = this.page.url() // we have to send NEXT page link in task

                currentPage++
            }
        } catch (err) {
            log.error("SearchAction: we catch something strange:", err)
            result_data.code = -1000
            result_data.data = JSON.stringify(result_data.data)
            return result_data
        }

        //log.debug("SearchAction: Reult Data: ", result_data)
        //log.debug("SearchAction: Users Data: ", result_data.data.arr)
        log.debug(
            "SearchAction: contacts scribed:",
            result_data.data.arr.length
        )
        result_data.data = JSON.stringify(result_data.data)
        return result_data
    }
}

module.exports = {
    SearchAction: SearchAction,
}
