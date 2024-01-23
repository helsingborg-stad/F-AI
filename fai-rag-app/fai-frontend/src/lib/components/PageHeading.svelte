<script lang="ts">
    import Table from "./Table.svelte"
    import Dropdown from "./Dropdown.svelte";


    let columns = [
        {key: 'name', title: 'Name'},
        {key: 'job', title: 'Job'},
        {key: 'color', title: 'Favorite Color'}
    ];

    let data = [
        {name: 'Cy Ganderton', job: 'Quality Control Specialist', color: 'Blue'},
    ];

    function handleHeaderClick(event) {
        console.log('Header clicked:', event.detail.column);
    }
</script>

<div class="w-full mb-4 flex items-center">
    <div>
        <div class="join join-horizontal">
            <input class="input input-bordered join-item">
            <button class="btn btn-neutral  join-item">Sök</button>
        </div>
    </div>
    <div class="ml-auto">
        <div class="space-x-2 flex items-center">
            <button class="btn btn-square btn-neutral">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                     class="lucide lucide-download">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" x2="12" y1="15" y2="3"/>
                </svg>
            </button>
            <button class="btn btn-neutral">Ny fråga</button>
            <button class="btn btn-neutral">Ny fråga</button>
        </div>
    </div>
</div>
<div class="card bg-base-200  max-w-screen-md mx-auto">
    <div class="card-actions">

        <div class="ml-auto join">
            <Dropdown buttonClass="btn btn-square join-item">
                <span slot="title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                         class="lucide lucide-download">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="7 10 12 15 17 10"/>
                        <line x1="12" x2="12" y1="15" y2="3"/>
                    </svg>
                </span>
                <div class="menu">
                    <ul>
                        <li><a href="#">Item 1</a></li>
                        <li><a href="#">Item 2</a></li>
                        <li class="disabled"><a href="#">Item 3</a></li>
                        <li><a href="#">Item 4</a></li>
                    </ul>
                </div>
            </Dropdown>
            <button class="join-item btn">

            </button>
        </div>
    </div>
    <div class="card-body p-2">
        <div class="min-h-80">
            <Table {columns} {data} on:headerClick={handleHeaderClick}>
                <div slot="header" let:column>
                    {column.title.toUpperCase()}
                </div>

                <div slot="cell" let:rowData let:column let:rowIndex let:colIndex>
                    {colIndex === 0 ? `Row ${rowIndex + 1}` : rowData[column.key]}
                </div>
            </Table>

        </div>
        <div class="card-actions flex justify-center">
            <div class="join">
                <button class="join-item btn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                         class="lucide lucide-chevron-left">
                        <path d="m15 18-6-6 6-6"/>
                    </svg>
                </button>
                <button class="join-item btn">1</button>
                <button class="join-item btn btn-active">2</button>
                <button class="join-item btn">3</button>
                <button class="join-item btn">4</button>
                <button class="join-item btn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                         class="lucide lucide-chevron-right">
                        <path d="m9 18 6-6-6-6"/>
                    </svg>
                </button>
            </div>
        </div>
    </div>
</div>
<div class="mb-96"></div>